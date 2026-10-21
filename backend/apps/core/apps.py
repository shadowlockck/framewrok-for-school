from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Загальні відомості та налаштування школи'

    def ready(self):
        from . import modules  # noqa: F401 - registers Django system checks
        import sys
        if sys.platform == 'win32':
            if hasattr(sys.stdout, 'reconfigure'):
                try:
                    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
                except Exception:
                    pass
            if hasattr(sys.stderr, 'reconfigure'):
                try:
                    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
                except Exception:
                    pass
