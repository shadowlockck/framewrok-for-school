#!/usr/bin/env python3
"""
CLI утиліта school-admin для швидкого створення та адміністрування сайтів шкіл.
Частина фреймворку django-school-framework.
"""

import sys
import os
import argparse
from pathlib import Path
from .frontend_templates import FRONTEND_TEMPLATES
from .frontend_site import APP_TSX, BASE_CSS, CONTRAST_CSS

# Windows UTF-8 console & ANSI color configuration
def configure_windows_encoding():
    """Налаштування UTF-8 кодування для Windows консолі та системного виводу."""
    if sys.platform == "win32":
        try:
            import os
            os.system("")  # Вмикає підтримку ANSI escape-послідовностей у Windows 10/11
        except Exception:
            pass
        if hasattr(sys.stdout, "reconfigure"):
            try:
                sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass
        if hasattr(sys.stderr, "reconfigure"):
            try:
                sys.stderr.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass
        if hasattr(sys.stdin, "reconfigure"):
            try:
                sys.stdin.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass

configure_windows_encoding()

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
    cwd = str(Path.cwd().resolve())
    if cwd not in sys.path:
        sys.path.insert(0, cwd)
    if not os.environ.get("DJANGO_SETTINGS_MODULE"):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    # Python 3.14+ compatibility patch
    try:
        if sys.version_info >= (3, 14):
            import django.template.context as _ctx
            def _safe_basecontext_copy(self):
                obj = self.__class__.__new__(self.__class__)
                obj.__dict__.update(self.__dict__)
                obj.dicts = self.dicts[:]
                return obj
            _ctx.BaseContext.__copy__ = _safe_basecontext_copy
    except Exception:
        pass

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
    (output_dir / "manage.py").write_text(manage_py_content, encoding="utf-8")
    try:
        (output_dir / "manage.py").chmod(0o755)
    except OSError:
        pass

    # 2. config/settings.py
    settings_content = f"""import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get('DEBUG', 'True') == 'True'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or ('django-insecure-local-development-only' if DEBUG else None)
if not SECRET_KEY:
    raise ImproperlyConfigured('Set DJANGO_SECRET_KEY when DEBUG=False')
ALLOWED_HOSTS = [host.strip() for host in os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1' if DEBUG else '').split(',') if host.strip()]
if not DEBUG and not ALLOWED_HOSTS:
    raise ImproperlyConfigured('Set ALLOWED_HOSTS when DEBUG=False')

# Enable proxy trust only when the trusted proxy replaces X-Forwarded-Proto.
SECURE_PROXY_SSL_HEADER = (
    ('HTTP_X_FORWARDED_PROTO', 'https')
    if os.environ.get('TRUST_X_FORWARDED_PROTO', 'False').lower() in ('true', '1', 'yes')
    else None
)
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', str(not DEBUG)).lower() in ('true', '1', 'yes')
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '0')) if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'False').lower() in ('true', '1', 'yes')
SECURE_HSTS_PRELOAD = os.environ.get('SECURE_HSTS_PRELOAD', 'False').lower() in ('true', '1', 'yes')

INSTALLED_APPS = [
    'apps.core',
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
        'NAME': BASE_DIR / 'db.sqlite3' if 'sqlite' in os.environ.get('DB_ENGINE', 'sqlite') else os.environ.get('DB_NAME', '{project_name}_db'),
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
REST_FRAMEWORK = {{
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}}
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',') if origin.strip()]
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

CSRF_TRUSTED_ORIGINS = [
    origin.strip() for origin in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if origin.strip()
]
if DEBUG:
    for port in range(5170, 5185):
        CSRF_TRUSTED_ORIGINS.append(f'http://localhost:{{port}}')
        CSRF_TRUSTED_ORIGINS.append(f'http://127.0.0.1:{{port}}')
    for port in (3000, 8000, 8001, 8080):
        CSRF_TRUSTED_ORIGINS.append(f'http://localhost:{{port}}')
        CSRF_TRUSTED_ORIGINS.append(f'http://127.0.0.1:{{port}}')
"""
    (output_dir / "config" / "settings.py").write_text(settings_content, encoding="utf-8")

    # 3. config/urls.py
    urls_content = """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from apps.core.views import PublicSchoolHomeView
from apps.core.modules import module_urlpatterns

urlpatterns = [
    path('', PublicSchoolHomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/core/', include('apps.core.urls')),
]
urlpatterns += module_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""
    (output_dir / "config" / "urls.py").write_text(urls_content, encoding="utf-8")

    # 4. config/__init__.py, wsgi.py, asgi.py
    init_content = """# Django School Framework Project
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

try:
    import sys
    if sys.version_info >= (3, 14):
        import django.template.context as _ctx
        def _safe_basecontext_copy(self):
            obj = self.__class__.__new__(self.__class__)
            obj.__dict__.update(self.__dict__)
            obj.dicts = self.dicts[:]
            return obj
        _ctx.BaseContext.__copy__ = _safe_basecontext_copy
except Exception:
    pass
"""
    (output_dir / "config" / "__init__.py").write_text(init_content, encoding="utf-8")

    wsgi_content = """import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
"""
    (output_dir / "config" / "wsgi.py").write_text(wsgi_content, encoding="utf-8")

    # 5. .env.example
    env_example = f"""DEBUG=True
DJANGO_SECRET_KEY=
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=
CSRF_TRUSTED_ORIGINS=
TRUST_X_FORWARDED_PROTO=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_HOST_PORT=3307
BACKEND_HOST_PORT=8000
FRONTEND_HOST_PORT=5173
"""
    (output_dir / ".env.example").write_text(env_example, encoding="utf-8")

    # 6. README.md
    readme_content = f"""# {project_name} — Офіційний вебсайт закладу освіти

Створено за допомогою **`django-school-framework`** (`school-admin`).
Сайт містить інструменти для перевірки оприлюднення інформації за **статтею 30 Закону України «Про освіту»**.

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

## Перед публікацією

Передайте через змінні середовища `DEBUG=False`, випадковий `DJANGO_SECRET_KEY`
і домени сайту в `ALLOWED_HOSTS`. За потреби задайте `CSRF_TRUSTED_ORIGINS`.
Файл `.env.example` є прикладом налаштувань; Django не завантажує його автоматично.
Налаштуйте HTTPS на сервері та виконайте `python manage.py check --deploy`.
За наявності довіреного проксі, який перезаписує X-Forwarded-Proto, встановіть
`TRUST_X_FORWARDED_PROTO=True`. HSTS вмикайте поступово через `SECURE_HSTS_SECONDS`.

## Фронтенд

Створіть React-сайт командою `school-admin create-frontend --template classic --output-dir frontend`.
Доступні варіанти: `classic` (офіційний), `editorial`
(редакційний) і `portal` (портал із бічним меню). Після створення виконайте `cd frontend`,
`npm install` і `npm run dev`. Вибраний макет можна змінювати у файлі
`src/index.css`; дані та навігація надходять з API школи.
"""
    (output_dir / "README.md").write_text(readme_content, encoding="utf-8")

    template = getattr(args, "frontend_template", None)
    if template:
        cmd_create_frontend(argparse.Namespace(
            output_dir=output_dir / "frontend", api_url="http://127.0.0.1:8000",
            force=False, template=template,
        ))

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


def cmd_create_frontend(args):
    """Створення готового сучасного React-фронтенду сайту школи."""
    template = getattr(args, "template", "classic")
    if template not in FRONTEND_TEMPLATES:
        raise ValueError(f"Unknown frontend template: {template}")
    target_dir = Path(args.output_dir or "frontend").resolve()

    if target_dir.exists() and any(target_dir.iterdir()):
        if not getattr(args, "force", False):
            print(f"{RED}Помилка: Директорія {target_dir} вже існує і не є порожньою. Використовуйте --force для перезапису.{RESET}")
            sys.exit(1)

    target_dir.mkdir(parents=True, exist_ok=True)
    if getattr(args, "force", False):
        # Older generated sites included these files. Vite loads a stale
        # PostCSS config even after the CSS and package.json are replaced.
        legacy_configs = {
            "postcss.config.js": """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
""",
            "tailwind.config.js": """/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
};
""",
        }
        for filename, generated_content in legacy_configs.items():
            config_path = target_dir / filename
            if config_path.is_file() and config_path.read_text(encoding="utf-8") == generated_content:
                config_path.unlink()
    src_dir = target_dir / "src"
    src_dir.mkdir(parents=True, exist_ok=True)

    # 1. package.json
    pkg_json = """{
  "name": "school-website-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "lucide-react": "^1.16.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@vitejs/plugin-react": "^4.3.4",
    "typescript": "~5.7.2",
    "vite": "^6.0.7"
  }
}
"""
    (target_dir / "package.json").write_text(pkg_json, encoding="utf-8")

    # 2. vite.config.ts
    backend_url = args.api_url or "http://127.0.0.1:8000"
    vite_conf = f"""import {{ defineConfig }} from 'vite';
import react from '@vitejs/plugin-react';

const backendUrl = process.env.VITE_BACKEND_URL || '{backend_url}';

export default defineConfig({{
  plugins: [react()],
  server: {{
    host: '0.0.0.0',
    port: 5173,
    proxy: {{
      '/api': {{
        target: backendUrl,
        changeOrigin: true,
      }},
      '/admin': {{
        target: backendUrl,
        changeOrigin: true,
      }},
      '/static': {{
        target: backendUrl,
        changeOrigin: true,
      }},
      '/media': {{
        target: backendUrl,
        changeOrigin: true,
      }},
    }},
  }},
}});
"""
    (target_dir / "vite.config.ts").write_text(vite_conf, encoding="utf-8")

    # 3. index.html
    index_html = """<!doctype html>
<html lang="uk">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Офіційний вебсайт закладу освіти</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""
    (target_dir / "index.html").write_text(index_html, encoding="utf-8")

    # 4. tsconfig.json
    tsconfig = """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true
  },
  "include": ["src"]
}
"""
    (target_dir / "tsconfig.json").write_text(tsconfig, encoding="utf-8")

    # 5. src/index.css
    index_css = BASE_CSS
    (src_dir / "index.css").write_text(
        index_css + FRONTEND_TEMPLATES[template]["css"] + CONTRAST_CSS,
        encoding="utf-8"
    )

    # 6. src/main.tsx
    main_tsx = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""
    (src_dir / "main.tsx").write_text(main_tsx, encoding="utf-8")

    # 7. src/App.tsx
    app_tsx = APP_TSX
    (src_dir / "App.tsx").write_text(
        app_tsx.replace("__SCHOOL_TEMPLATE__", template).replace(
            "__SCHOOL_TEMPLATE_LABEL__", FRONTEND_TEMPLATES[template]["label"]
        ), encoding="utf-8"
    )

    print(f"\n{GREEN}{BOLD}✓ Готовий React-фронтенд «{FRONTEND_TEMPLATES[template]['name']}» створено у {target_dir}!{RESET}\n")
    print(f"Наступні кроки для запуску сайту:")
    print(f"  {CYAN}cd {args.output_dir or 'frontend'}{RESET}")
    print(f"  {CYAN}npm install{RESET}")
    print(f"  {CYAN}npm run dev{RESET}\n")
    print(f"Сайт буде доступний за адресою: {BOLD}http://localhost:5173{RESET}\n")


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
    p_start.add_argument("--frontend-template", choices=FRONTEND_TEMPLATES,
                         help="Одразу створити фронтенд: classic, editorial або portal")

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

    # 5. create-frontend
    p_front = subparsers.add_parser("create-frontend", help="Створити готовий React-фронтенд сайту школи")
    p_front.add_argument("--output-dir", "-o", default="frontend", help="Назва папки фронтенду (за замовчуванням frontend)")
    p_front.add_argument("--api-url", default="http://127.0.0.1:8000", help="URL бекенд API")
    p_front.add_argument("--template", choices=FRONTEND_TEMPLATES, default="classic",
                         help="Макет сайту: classic (типовий), editorial або portal")
    p_front.add_argument("--force", "-f", action="store_true", help="Перезаписати файли, якщо директорія вже існує")

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
    elif args.subcommand == "create-frontend":
        cmd_create_frontend(args)


if __name__ == "__main__":
    main()
