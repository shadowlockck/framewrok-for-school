import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    """Django command that pauses execution until the database is available"""

    def handle(self, *args, **options):
        self.stdout.write('Очікування з’єднання з базою даних...')
        db_conn = None
        retries = 30
        while not db_conn and retries > 0:
            try:
                db_conn = connections['default']
                db_conn.cursor()
                self.stdout.write(self.style.SUCCESS('База даних доступна!'))
                return
            except OperationalError:
                retries -= 1
                self.stdout.write(f'База даних поки що недоступна, спроба через 1с... (залишилось {retries})')
                time.sleep(1)

        if not db_conn:
            self.stdout.write(self.style.ERROR('Не вдалося з’єднатися з базою даних.'))
            exit(1)
