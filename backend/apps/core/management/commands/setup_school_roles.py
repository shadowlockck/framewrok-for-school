"""Create or reconcile editor groups after Django's post_migrate permissions exist."""

from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db import connections, router, transaction
from django.db.utils import DatabaseError

from apps.core.roles import group_name, role_specs


class Command(BaseCommand):
    help = 'Створити або синхронізувати редакторські групи шкільного фреймворку.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Показати зміни без запису до БД.')
        parser.add_argument('--database', default='default', help='Псевдонім БД з таблицями auth.')

    def handle(self, *args, **options):
        alias = options['database']
        if alias not in connections:
            raise CommandError(f'Невідома база даних: {alias}.')
        for model in (Group, Permission, ContentType):
            if not router.allow_migrate_model(alias, model):
                raise CommandError(f'{model._meta.label} не дозволено в БД {alias}; auth має бути в одній БД.')

        db = connections[alias]
        needed_tables = {model._meta.db_table for model in (Group, Permission, ContentType)}
        needed_tables.add(Group.permissions.through._meta.db_table)
        try:
            missing_tables = needed_tables - set(db.introspection.table_names())
            if missing_tables:
                raise CommandError('Відсутні таблиці авторизації. Спочатку виконайте manage.py migrate.')

            specs = role_specs()
            requested = {
                (model._meta.app_label, model._meta.model_name, f'{action}_{model._meta.model_name}')
                for spec in specs.values() for label, actions in spec.models.items()
                for model in (apps.get_model(label),) for action in actions
            }
            available = {
                (p.content_type.app_label, p.content_type.model, p.codename): p
                for p in Permission.objects.using(alias).select_related('content_type').filter(
                    content_type__app_label__in={key[0] for key in requested}
                )
            }
            missing = requested - available.keys()
            if missing:
                names = ', '.join('.'.join(item) for item in sorted(missing))
                raise CommandError(f'Відсутні дозволи {names}. Спочатку виконайте manage.py migrate.')

            groups = {group.name: group for group in Group.objects.using(alias).filter(
                name__in=[group_name(spec) for spec in specs.values()]
            )}
            changes = []
            for spec in specs.values():
                name = group_name(spec)
                expected = {
                    available[(model._meta.app_label, model._meta.model_name,
                               f'{action}_{model._meta.model_name}')].pk
                    for label, actions in spec.models.items()
                    for model in (apps.get_model(label),) for action in actions
                }
                group = groups.get(name)
                if group is None and not spec.models:
                    continue
                current = set(group.permissions.using(alias).values_list('pk', flat=True)) if group else set()
                if group is None or current != expected:
                    additions = expected - current
                    removals = current - expected
                    changes.append((name, group, expected, additions, removals))

            if options['dry_run']:
                permission_names = {
                    permission.pk: f'{permission.content_type.app_label}.{permission.codename}'
                    for permission in Permission.objects.using(alias).select_related('content_type').filter(
                        pk__in={pk for _, _, _, additions, removals in changes for pk in additions | removals}
                    )
                }
                for name, group, _, additions, removals in changes:
                    self.stdout.write(f'{name}: {"створити; " if group is None else ""}'
                                      f'додати {len(additions)}, прибрати {len(removals)} дозволів.')
                    for label, ids in (('+', additions), ('-', removals)):
                        for pk in sorted(ids, key=lambda value: permission_names[value]):
                            self.stdout.write(f'  {label} {permission_names[pk]}')
            else:
                with transaction.atomic(using=alias):
                    for name, group, expected, additions, removals in changes:
                        if group is None:
                            group = Group.objects.db_manager(alias).create(name=name)
                        group.permissions.set(expected)
                        self.stdout.write(f'{name}: оновлено ({len(additions)} додано, '
                                          f'{len(removals)} прибрано).')
            self.stdout.write(f'Готово: {len(changes)} груп потребували змін.'
                              if options['dry_run'] else f'Готово: {len(changes)} груп оновлено.')
            self.stdout.write('Призначайте групи працівникам окремо; для входу в адмінку потрібен is_staff.')
        except DatabaseError as exc:
            raise CommandError('Не вдалося прочитати таблиці auth. Перевірте підключення й виконайте міграції.') from exc
