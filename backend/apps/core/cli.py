#!/usr/bin/env python3
"""
CLI утиліта school-admin для швидкого створення та адміністрування сайтів шкіл.
Частина фреймворку django-school-framework.
"""

import sys
import os
import argparse
from pathlib import Path

# ANSI colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def setup_django_environment():
    """Ініціалізація оточення Django для команд, що працюють з БД."""
    if not os.environ.get("DJANGO_SETTINGS_MODULE"):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    import django
    django.setup()


def cmd_startproject(args):
    """Створення нового проєкту закладу освіти з готовою структурою."""
    project_name = args.name
    output_dir = Path(args.output_dir or ".").resolve() / project_name

    if output_dir.exists() and any(output_dir.iterdir()):
        print(f"{RED}Помилка: Директорія {output_dir} вже існує і не є порожньою.{RESET}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "config").mkdir(parents=True, exist_ok=True)
    (output_dir / "media").mkdir(parents=True, exist_ok=True)
    (output_dir / "static").mkdir(parents=True, exist_ok=True)

    # 1. manage.py
    manage_py_content = """#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не вдалося імпортувати Django. Переконайтеся, що віртуальне оточення активоване."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
"""
    (output_dir / "manage.py").write_text(manage_py_content)
    (output_dir / "manage.py").chmod(0o755)

    # 2. config/settings.py
    settings_content = f"""import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-school-framework-demo-key-change-in-prod')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'corsheaders',
    'drf_spectacular',

    # School Framework Modules
    'apps.core',
    'apps.legal',
    'apps.admissions',
    'apps.nutrition',
    'apps.safety',
    'apps.news',
    'apps.schedule',
    'apps.gallery',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {{
    'default': {{
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': BASE_DIR / 'db.sqlite3' if os.environ.get('DB_ENGINE', '').endswith('sqlite3') else os.environ.get('DB_NAME', '{project_name}_db'),
    }}
}}

LANGUAGE_CODE = 'uk'
TIME_ZONE = 'Europe/Kyiv'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True
"""
    (output_dir / "config" / "settings.py").write_text(settings_content)

    # 3. config/urls.py
    urls_content = """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/core/', include('apps.core.urls')),
    path('api/v1/legal/', include('apps.legal.urls')),
    path('api/v1/admissions/', include('apps.admissions.urls')),
    path('api/v1/nutrition/', include('apps.nutrition.urls')),
    path('api/v1/safety/', include('apps.safety.urls')),
    path('api/v1/news/', include('apps.news.urls')),
    path('api/v1/schedule/', include('apps.schedule.urls')),
    path('api/v1/gallery/', include('apps.gallery.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
    (output_dir / "config" / "urls.py").write_text(urls_content)

    # 4. config/__init__.py, wsgi.py, asgi.py
    (output_dir / "config" / "__init__.py").write_text("# Django School Framework Project\n")

    wsgi_content = """import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
"""
    (output_dir / "config" / "wsgi.py").write_text(wsgi_content)

    # 5. .env.example
    env_example = f"""DEBUG=True
DJANGO_SECRET_KEY=change-me-in-production
DB_ENGINE=django.db.backends.sqlite3
DB_NAME={project_name}_db
DB_HOST_PORT=3307
BACKEND_HOST_PORT=8000
FRONTEND_HOST_PORT=5173
"""
    (output_dir / ".env.example").write_text(env_example)

    # 6. README.md
    readme_content = f"""# {project_name} — Офіційний вебсайт закладу освіти

Створено за допомогою **`django-school-framework`** (`school-admin`).
Сайт повністю відповідає вимогам **статті 30 Закону України «Про освіту»**.

## Швидкий старт:

```bash
# 1. Встановити залежності
pip install django-school-framework

# 2. Застосувати міграції
python manage.py migrate

# 3. Створити профіль закладу
school-admin create-school "{project_name}" --edrpou 12345678

# 4. Перевірити рівень відповідності закону
school-admin check-compliance

# 5. Запустити сервер розробки
python manage.py runserver
```
"""
    (output_dir / "README.md").write_text(readme_content)

    print(f"\n{GREEN}{BOLD}✓ Проєкт закладу освіти успішно створено у {output_dir}!{RESET}\n")
    print(f"Наступні кроки:")
    print(f"  {CYAN}cd {project_name}{RESET}")
    print(f"  {CYAN}python manage.py migrate{RESET}")
    print(f"  {CYAN}school-admin create-school \"{project_name}\" --edrpou 12345678{RESET}")
    print(f"  {CYAN}python manage.py runserver{RESET}\n")


def cmd_create_school(args):
    """Створення чи оновлення профілю школи з реквізитами та темами."""
    setup_django_environment()
    from apps.core.models import SchoolProfile, ThemeSettings

    profile, created = SchoolProfile.objects.get_or_create(
        id=1,
        defaults={
            'name': args.name,
            'short_name': args.short_name or args.name,
            'edrpou': args.edrpou or '00000000',
            'founder': args.founder or 'Орган місцевого самоврядування',
            'address': args.address or f"м. {args.city or 'Київ'}",
            'phone': args.phone or "+380 44 000-00-00",
            'email': args.email or "school@education.gov.ua",
            'licensed_capacity': args.capacity or 1000,
            'actual_students': args.actual or 900,
            'education_language': args.language or "Українська",
        }
    )

    if not created:
        profile.name = args.name
        if args.short_name: profile.short_name = args.short_name
        if args.edrpou: profile.edrpou = args.edrpou
        if args.founder: profile.founder = args.founder
        if args.address: profile.address = args.address
        if args.phone: profile.phone = args.phone
        if args.email: profile.email = args.email
        if args.capacity: profile.licensed_capacity = args.capacity
        if args.actual: profile.actual_students = args.actual
        if args.language: profile.education_language = args.language
        profile.save()

    # Створюємо чи оновлюємо параметри теми
    ThemeSettings.objects.get_or_create(
        school=profile,
        defaults={
            'primary_color': args.primary_color or '#1e3a8a',
            'secondary_color': '#059669',
            'accent_color': '#d97706',
        }
    )

    action_text = "створено" if created else "оновлено"
    print(f"\n{GREEN}{BOLD}✓ Профіль школи успішно {action_text}!{RESET}")
    print(f"  {BOLD}Заклад:{RESET} {profile.name} (ЄДРПОУ {profile.edrpou})")
    print(f"  {BOLD}Засновник:{RESET} {profile.founder}")
    print(f"  {BOLD}Мова навчання:{RESET} {profile.education_language}")
    print(f"  {BOLD}Місткість:{RESET} ліцензія {profile.licensed_capacity}, факт {profile.actual_students}\n")


def cmd_check_compliance(args):
    """Перевірка виконання ст. 30 ЗУ «Про освіту» прямо в терміналі."""
    setup_django_environment()
    from apps.core.compliance import ComplianceAuditor
    import json

    report = ComplianceAuditor.get_audit_report()

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        sys.exit(0 if report['is_fully_compliant'] else 1)

    score = report['score']
    bar_width = 30
    filled = int(bar_width * (score / 100))
    bar = "█" * filled + "░" * (bar_width - filled)

    color = GREEN if report['is_fully_compliant'] else (YELLOW if score >= 60 else RED)

    print("\n" + "=" * 65)
    print(f"{BOLD} МОНІТОР ІНФОРМАЦІЙНОЇ ВІДКРИТОСТІ (СТ. 30 ЗУ «ПРО ОСВІТУ») {RESET}")
    print("=" * 65)

    print(f"\n{BOLD}Рівень відповідності:{RESET} {color}{BOLD}[{bar}] {score}%{RESET}")
    print(f"Критерії: {GREEN}✓ {report['passed_count']} виконано{RESET} | {YELLOW}⚠ {report['warning_count']} до уваги{RESET} | {RED}✕ {report['danger_count']} порушень{RESET}\n")

    if report['warnings']:
        print(f"{YELLOW}{BOLD}⚠️ ОПЕРАТИВНІ ПОПЕРЕДЖЕННЯ:{RESET}")
        for w in report['warnings']:
            print(f"  {YELLOW}• {w}{RESET}")
        print()

    print(f"{BOLD}ЧЕК-ЛИСТ ВИМОГ СТАТТІ 30:{RESET}")
    for c in report['checks']:
        if c['status'] == 'ok':
            icon = f"{GREEN}✓{RESET}"
        elif c['status'] == 'warning':
            icon = f"{YELLOW}⚠{RESET}"
        else:
            icon = f"{RED}✕{RESET}"
        print(f"  {icon} {BOLD}{c['title']}{RESET} ({c['law_ref']})")
        print(f"     Стан: {c['message']}")

    print("\n" + "=" * 65)
    if report['is_fully_compliant']:
        print(f"{GREEN}{BOLD}✓ Заклад повністю відповідає вимогам інформаційної прозорості!{RESET}\n")
        sys.exit(0)
    else:
        print(f"{YELLOW}Порада: перейдіть в адмін-панель (/admin/), щоб завантажити відсутні документи.{RESET}\n")
        sys.exit(0 if score >= 60 else 1)


def cmd_seed_data(args):
    """Наповнення бази демонстраційними даними для швидкого тестування."""
    setup_django_environment()
    from django.core.management import call_command
    print(f"{CYAN}Генерація тестових даних школи...{RESET}")
    try:
        call_command('seed_school_data')
        print(f"{GREEN}{BOLD}✓ Демонстраційні дані успішно завантажено!{RESET}")
    except Exception as e:
        print(f"{RED}Помилка генерації даних: {e}{RESET}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog="school-admin",
        description="CLI-утиліта для швидкого створення та перевірки сайтів шкіл на базі django-school-framework",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Команди")

    # 1. startproject
    p_start = subparsers.add_parser("startproject", help="Створити новий проект шкільного сайту")
    p_start.add_argument("name", help="Назва проєкту/директорії (напр. lyceum_1)")
    p_start.add_argument("--output-dir", "-o", help="Цільова батьківська директорія")

    # 2. create-school
    p_school = subparsers.add_parser("create-school", help="Створити або оновити профіль закладу освіти")
    p_school.add_argument("name", help="Офіційна назва закладу (напр. «Ліцей №1 м. Києва»)")
    p_school.add_argument("--short-name", help="Скорочена назва")
    p_school.add_argument("--edrpou", help="Код ЄДРПОУ (8 цифр)")
    p_school.add_argument("--founder", help="Засновник закладу")
    p_school.add_argument("--city", help="Місто/населений пункт")
    p_school.add_argument("--address", help="Повна адреса")
    p_school.add_argument("--phone", help="Контактний телефон")
    p_school.add_argument("--email", help="Офіційний email")
    p_school.add_argument("--capacity", type=int, help="Ліцензований обсяг")
    p_school.add_argument("--actual", type=int, help="Фактична кількість учнів")
    p_school.add_argument("--language", help="Мова освітнього процесу")
    p_school.add_argument("--primary-color", help="Основний брендовий колір (hex, напр. #1e3a8a)")

    # 3. check-compliance
    p_comp = subparsers.add_parser("check-compliance", help="Перевірити виконання ст. 30 ЗУ «Про освіту»")
    p_comp.add_argument("--json", action="store_true", help="Вивести звіт у форматі JSON (для CI/CD)")

    # 4. seed-data
    subparsers.add_parser("seed-data", help="Заповнити базу реалістичними зразками даних для тесту")

    args = parser.parse_args()

    if not args.subcommand:
        parser.print_help()
        sys.exit(0)

    if args.subcommand == "startproject":
        cmd_startproject(args)
    elif args.subcommand == "create-school":
        cmd_create_school(args)
    elif args.subcommand == "check-compliance":
        cmd_check_compliance(args)
    elif args.subcommand == "seed-data":
        cmd_seed_data(args)


if __name__ == "__main__":
    main()
