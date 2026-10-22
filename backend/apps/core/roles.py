"""Explicit permissions for the built-in school editor groups."""

from dataclasses import dataclass

from .modules import installed_modules


CRUD = ('view', 'add', 'change', 'delete')
VIEW_CHANGE = ('view', 'change')


@dataclass(frozen=True)
class RoleSpec:
    name: str
    modules: tuple[str, ...]
    models: dict[str, tuple[str, ...]]


SECTION_ROLES = {
    'news_editor': RoleSpec('Редактор новин', ('news',), {
        'news.NewsCategory': CRUD, 'news.NewsArticle': CRUD,
    }),
    'legal_editor': RoleSpec('Редактор документів і відомостей', ('legal',), {
        'legal.LegalDocumentCategory': CRUD, 'legal.LegalDocument': CRUD,
        'legal.StaffMember': CRUD, 'legal.Vacancy': CRUD,
    }),
    'finance_editor': RoleSpec('Редактор фінансової звітності', ('legal',), {
        'legal.FinancialReport': CRUD,
    }),
    'admissions_editor': RoleSpec('Редактор вступу', ('admissions',), {
        'admissions.ServiceTerritory': CRUD, 'admissions.ClassCapacity': CRUD,
        'admissions.EnrolledStudent': CRUD, 'admissions.AdmissionLottery': CRUD,
    }),
    'nutrition_editor': RoleSpec('Редактор харчування', ('nutrition',), {
        'nutrition.CateringProvider': CRUD, 'nutrition.DailyMenu': CRUD,
    }),
    'schedule_editor': RoleSpec('Редактор розкладу', ('schedule', 'admissions'), {
        'schedule.BellSchedule': CRUD, 'schedule.LessonSchedule': CRUD,
        'admissions.ClassCapacity': ('view',),
    }),
    'gallery_editor': RoleSpec('Редактор галереї', ('gallery',), {
        'gallery.PhotoAlbum': CRUD, 'gallery.GalleryPhoto': CRUD,
    }),
    'safety_editor': RoleSpec('Редактор публічного розділу безпеки', ('safety',), {
        'safety.AntiBullyingPolicy': CRUD,
    }),
    'reports_reviewer': RoleSpec('Відповідальний за конфіденційні звернення', ('safety',), {
        'safety.ConfidentialReport': VIEW_CHANGE,
    }),
}

CORE_MODELS = {
    'core.SchoolProfile': VIEW_CHANGE,
    'core.ThemeSettings': VIEW_CHANGE,
}
GROUP_PREFIX = 'Шкільний фреймворк: '


def role_specs():
    """Return only built-in roles; disabled modules produce empty permissions."""
    enabled = installed_modules()
    content_models = dict(CORE_MODELS)
    for key, spec in SECTION_ROLES.items():
        if key != 'reports_reviewer' and all(enabled[module] for module in spec.modules):
            for label, operations in spec.models.items():
                content_models[label] = tuple(dict.fromkeys(content_models.get(label, ()) + operations))

    return {
        'content_admin': RoleSpec('Головний редактор', (), content_models),
        **{
            key: RoleSpec(spec.name, spec.modules,
                          spec.models if all(enabled[module] for module in spec.modules) else {})
            for key, spec in SECTION_ROLES.items()
        },
    }


def group_name(spec):
    return GROUP_PREFIX + spec.name
