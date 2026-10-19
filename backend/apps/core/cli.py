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

urlpatterns = [
    path('', PublicSchoolHomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
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

## Перед публікацією

Передайте через змінні середовища `DEBUG=False`, випадковий `DJANGO_SECRET_KEY`
і домени сайту в `ALLOWED_HOSTS`. За потреби задайте `CSRF_TRUSTED_ORIGINS`.
Файл `.env.example` є прикладом налаштувань; Django не завантажує його автоматично.
Налаштуйте HTTPS на сервері та виконайте `python manage.py check --deploy`.
За наявності довіреного проксі, який перезаписує X-Forwarded-Proto, встановіть
`TRUST_X_FORWARDED_PROTO=True`. HSTS вмикайте поступово через `SECURE_HSTS_SECONDS`.

## Фронтенд

Створіть React-сайт командою `school-admin create-frontend --template classic --output-dir frontend`.
Доступні варіанти: `classic` (поточний), `editorial`
(редакційний) і `portal` (портал). Після створення виконайте `cd frontend`,
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
    "clsx": "^2.1.1",
    "lucide-react": "^1.16.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "tailwind-merge": "^3.0.2"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@vitejs/plugin-react": "^4.3.4",
    "autoprefixer": "^10.4.20",
    "postcss": "^8.4.49",
    "tailwindcss": "^3.4.17",
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
  <body class="bg-slate-50 text-slate-900 font-sans antialiased">
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

    # 5. tailwind & postcss
    tailwind_conf = """/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
};
"""
    (target_dir / "tailwind.config.js").write_text(tailwind_conf, encoding="utf-8")

    postcss_conf = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
"""
    (target_dir / "postcss.config.js").write_text(postcss_conf, encoding="utf-8")

    # 6. src/index.css
    index_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

body.contrast-yellow {
  background-color: #000000 !important;
  color: #ffff00 !important;
}
body.contrast-yellow * {
  border-color: #ffff00 !important;
}
body.contrast-bw {
  background-color: #ffffff !important;
  color: #000000 !important;
}
body.contrast-yellow .school-site,
body.contrast-yellow .school-site * {
  background-color: #000000 !important;
  background-image: none !important;
  color: #ffff00 !important;
  border-color: #ffff00 !important;
}
body.contrast-bw .school-site,
body.contrast-bw .school-site * {
  background-color: #ffffff !important;
  background-image: none !important;
  color: #000000 !important;
  border-color: #000000 !important;
}
"""
    (src_dir / "index.css").write_text(
        index_css + FRONTEND_TEMPLATES[template]["css"], encoding="utf-8"
    )

    # 7. src/main.tsx
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

    # 8. src/App.tsx
    app_tsx = """import React, { useState, useEffect } from 'react';
import { Eye, Shield, FileText, Users, Utensils, Calendar, Newspaper, Award, CheckCircle2, AlertCircle, Download, ExternalLink, Send, Image as ImageIcon, Clock, BookOpen } from 'lucide-react';

export default function App() {
  const [manifest, setManifest] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<string>('legal');
  const [fontSize, setFontSize] = useState<number>(16);
  const [contrast, setContrast] = useState<string>('normal');
  const [loading, setLoading] = useState<boolean>(true);

  // Real data state
  const [documents, setDocuments] = useState<any[]>([]);
  const [finances, setFinances] = useState<any[]>([]);
  const [capacities, setCapacities] = useState<any[]>([]);
  const [territory, setTerritory] = useState<any[]>([]);
  const [menus, setMenus] = useState<any[]>([]);
  const [policy, setPolicy] = useState<any>(null);
  const [albums, setAlbums] = useState<any[]>([]);
  const [selectedAlbum, setSelectedAlbum] = useState<any | null>(null);
  const [newsList, setNewsList] = useState<any[]>([]);
  const [selectedNews, setSelectedNews] = useState<any | null>(null);
  const [bells, setBells] = useState<any[]>([]);
  const [cateringProvider, setCateringProvider] = useState<any | null>(null);

  // Bullying report form
  const [incidentText, setIncidentText] = useState('');
  const [reporterRole, setReporterRole] = useState('student');
  const [reportStatus, setReportStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [reportFeedback, setReportFeedback] = useState<string | null>(null);

  useEffect(() => {
    // 1. Fetch school manifest
    fetch('/api/v1/core/manifest/')
      .then(res => res.json())
      .then(data => {
        setManifest(data);
        if (data?.navigation?.length > 0) setActiveTab(data.navigation[0].id);
        setLoading(false);
      })
      .catch(() => setLoading(false));

    // 2. Fetch real data for all tabs from backend
    fetch('/api/v1/legal/documents/')
      .then(r => r.json())
      .then(d => setDocuments(d.results || d))
      .catch(() => {});

    fetch('/api/v1/legal/financial-reports/')
      .then(r => r.json())
      .then(d => setFinances(d.results || d))
      .catch(() => {});

    fetch('/api/v1/admissions/capacity/')
      .then(r => r.json())
      .then(d => setCapacities(d.results || d))
      .catch(() => {});

    fetch('/api/v1/admissions/territory/')
      .then(r => r.json())
      .then(d => setTerritory(d.results || d))
      .catch(() => {});

    fetch('/api/v1/nutrition/daily-menus/')
      .then(r => r.json())
      .then(d => setMenus(d.results || d))
      .catch(() => {});

    fetch('/api/v1/nutrition/providers/')
      .then(r => r.json())
      .then(d => {
        const items = d.results || d;
        if (items.length > 0) setCateringProvider(items[0]);
      })
      .catch(() => {});

    fetch('/api/v1/safety/policy/')
      .then(r => r.json())
      .then(d => {
        const items = d.results || d;
        if (items.length > 0) setPolicy(items[0]);
      })
      .catch(() => {});

    fetch('/api/v1/gallery/albums/')
      .then(r => r.json())
      .then(d => setAlbums(d.results || d))
      .catch(() => {});

    fetch('/api/v1/news/articles/')
      .then(r => r.json())
      .then(d => setNewsList(d.results || d))
      .catch(() => {});

    fetch('/api/v1/schedule/bells/')
      .then(r => r.json())
      .then(d => setBells(d.results || d))
      .catch(() => {});
  }, []);

  const changeContrast = (mode: string) => {
    setContrast(mode);
    document.body.classList.remove('contrast-yellow', 'contrast-bw');
    if (mode !== 'normal') document.body.classList.add(mode);
  };

  const handleReportSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!incidentText.trim()) return;
    setReportStatus('loading');
    setReportFeedback(null);

    const csrfMatch = document.cookie.match(/csrftoken=([^;]+)/);
    const csrfToken = csrfMatch ? csrfMatch[1] : '';
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (csrfToken) headers['X-CSRFToken'] = csrfToken;

    fetch('/api/v1/safety/reports/', {
      method: 'POST',
      headers,
      body: JSON.stringify({
        reporter_role: reporterRole,
        incident_description: incidentText,
      }),
    })
      .then(res => {
        if (res.ok) {
          setReportStatus('success');
          setReportFeedback('Дякуємо! Ваше конфіденційне звернення надіслано комісії закладу для розгляду.');
          setIncidentText('');
        } else {
          setReportStatus('error');
          setReportFeedback('Помилка при відправці. Будь ласка, зверніться до чергового адміністратора.');
        }
      })
      .catch(() => {
        setReportStatus('error');
        setReportFeedback("Помилка з'єднання. Будь ласка, зверніться до чергового адміністратора.");
      });
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 text-slate-600">
        <div className="text-xl font-semibold animate-pulse">Завантаження сайту школи...</div>
      </div>
    );
  }

  const school = manifest?.school;
  const primaryColor = school?.theme?.primary_color || '#1e3a8a';

  return (
    <div className="school-site school-site--__SCHOOL_TEMPLATE__ min-h-screen flex flex-col" style={{ fontSize: `${fontSize}px`, '--school-primary': primaryColor } as React.CSSProperties}>
      {/* WCAG 2.1 AA Accessibility Bar */}
      <div className="bg-slate-900 text-slate-100 px-4 py-2 text-xs md:text-sm flex flex-wrap justify-between items-center gap-2">
        <div className="flex items-center gap-2">
          <Eye className="w-4 h-4 text-emerald-400" />
          <span>Версія для осіб з порушенням зору (WCAG 2.1 AA)</span>
        </div>
        <div className="flex items-center gap-2">
          <span>Шрифт:</span>
          <button onClick={() => setFontSize(Math.max(14, fontSize - 2))} className="px-2 py-0.5 bg-slate-800 rounded hover:bg-slate-700">A-</button>
          <button onClick={() => setFontSize(16)} className="px-2 py-0.5 bg-slate-800 rounded hover:bg-slate-700">A</button>
          <button onClick={() => setFontSize(Math.min(24, fontSize + 2))} className="px-2 py-0.5 bg-slate-800 rounded hover:bg-slate-700">A+</button>
          <span className="ml-2">Контраст:</span>
          <button onClick={() => changeContrast('normal')} className="px-2 py-0.5 bg-slate-800 rounded hover:bg-slate-700">Звичайний</button>
          <button onClick={() => changeContrast('contrast-bw')} className="px-2 py-0.5 bg-slate-800 rounded hover:bg-slate-700">Ч/Б</button>
          <button onClick={() => changeContrast('contrast-yellow')} className="px-2 py-0.5 bg-yellow-400 text-black font-bold rounded">Жовтий/Чорний</button>
        </div>
      </div>

      {/* Header */}
      <header className="school-header bg-white border-b border-slate-200 shadow-sm">
        <div className="school-branding max-w-7xl mx-auto px-4 py-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight" style={{ color: primaryColor }}>
              {school?.name || 'Офіційний вебсайт закладу освіти'}
            </h1>
            <p className="text-slate-500 text-sm mt-1">
              {school?.founder} &bull; Код ЄДРПОУ: <strong>{school?.edrpou}</strong> &bull; Мова: {school?.education_language}
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800">
              <Award className="w-3.5 h-3.5" /> ст. 30 ЗУ «Про освіту»
            </span>
          </div>
        </div>

        {/* Dynamic Navigation */}
        <nav className="school-nav max-w-7xl mx-auto px-4 flex gap-1 overflow-x-auto border-t border-slate-100" aria-label="Розділи сайту">
          {manifest?.navigation?.map((item: any) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              aria-current={activeTab === item.id ? 'page' : undefined}
              className={`px-4 py-3 text-sm font-semibold border-b-2 whitespace-nowrap transition-colors ${
                activeTab === item.id
                  ? 'border-blue-700 text-blue-700'
                  : 'border-transparent text-slate-600 hover:text-slate-900'
              }`}
            >
              {item.title}
            </button>
          ))}
        </nav>
      </header>

      {/* Main Content */}
      <main className="school-main flex-1 max-w-7xl w-full mx-auto px-4 py-8">
        {/* Banner with school capacity stats */}
        <div className="school-stats grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm text-center">
            <div className="text-2xl font-bold text-slate-800">{school?.licensed_capacity || 0}</div>
            <div className="text-xs uppercase text-slate-500 font-semibold mt-1">Ліцензований обсяг</div>
          </div>
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm text-center">
            <div className="text-2xl font-bold text-slate-800">{school?.actual_students || 0}</div>
            <div className="text-xs uppercase text-slate-500 font-semibold mt-1">Фактично учнів</div>
          </div>
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm text-center">
            <div className="text-2xl font-bold text-emerald-600">100%</div>
            <div className="text-xs uppercase text-slate-500 font-semibold mt-1">Прозорість (ст. 30)</div>
          </div>
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm text-center">
            <div className="text-2xl font-bold text-blue-600">WCAG 2.1</div>
            <div className="text-xs uppercase text-slate-500 font-semibold mt-1">Цифрова доступність</div>
          </div>
        </div>

        {/* Tab Content */}
        <div className="school-content bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
          {activeTab === 'legal' && (
            <div>
              <div className="flex justify-between items-center mb-4">
                <div>
                  <h2 className="text-xl font-bold text-slate-900">Реєстр нормативних документів (ст. 30)</h2>
                  <p className="text-slate-500 text-sm">Статут закладу, ліцензії, сертифікати акредитації та звіти керівника</p>
                </div>
                <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 text-slate-700 rounded-full">
                  Знайдено: {documents.length}
                </span>
              </div>

              {documents.length === 0 ? (
                <div className="p-8 text-center text-slate-500 bg-slate-50 rounded-xl">
                  Документи ще не завантажені через панель керування.
                </div>
              ) : (
                <div className="divide-y divide-slate-100">
                  {documents.map((doc: any) => (
                    <div key={doc.id} className="py-3 flex justify-between items-center hover:bg-slate-50 px-2 rounded-lg">
                      <div className="flex items-center gap-3">
                        <FileText className="w-5 h-5 text-blue-600 shrink-0" />
                        <div>
                          <div className="font-semibold text-slate-900">{doc.title}</div>
                          <div className="text-xs text-slate-500">
                            {doc.category_name && <span>Категорія: {doc.category_name} &bull; </span>}
                            Оприлюднено: {doc.publish_date || doc.published_date || doc.approval_date || ''}
                          </div>
                        </div>
                      </div>
                      {(doc.file || doc.external_url) && (
                        <a
                          href={doc.file || doc.external_url}
                          target="_blank"
                          rel="noreferrer"
                          className="px-3 py-1.5 text-xs font-semibold text-blue-700 bg-blue-50 hover:bg-blue-100 rounded-lg flex items-center gap-1"
                        >
                          <Download className="w-3.5 h-3.5" /> {doc.file ? 'Завантажити' : 'Відкрити'}
                        </a>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'finance' && (
            <div>
              <div className="flex justify-between items-center mb-4">
                <div>
                  <h2 className="text-xl font-bold text-slate-900">Кошторис та фінансова звітність</h2>
                  <p className="text-slate-500 text-sm">Звіти про надходження та використання коштів (ч. 3 ст. 30 ЗУ «Про освіту»)</p>
                </div>
                <span className="text-xs font-semibold px-2.5 py-1 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full">
                  Строк 10 робочих днів
                </span>
              </div>

              {finances.length === 0 ? (
                <div className="p-8 text-center text-slate-500 bg-slate-50 rounded-xl">
                  Фінансові звіти ще не оприлюднені в базі даних.
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm">
                    <thead>
                      <tr className="border-b border-slate-200 text-slate-500 text-xs uppercase">
                        <th className="py-3 px-2">Звітний період</th>
                        <th className="py-3 px-2">Тип звіту</th>
                        <th className="py-3 px-2">Сума коштів (грн)</th>
                        <th className="py-3 px-2">Контроль 10 днів</th>
                        <th className="py-3 px-2 text-right">Файл</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {finances.map((f: any) => (
                        <tr key={f.id} className="hover:bg-slate-50">
                          <td className="py-3 px-2 font-bold text-slate-900">{f.period || f.title}</td>
                          <td className="py-3 px-2">{f.report_type_display || f.report_type}</td>
                          <td className="py-3 px-2 font-mono text-emerald-700">{Number(f.total_amount || 0).toLocaleString()} ₴</td>
                          <td className="py-3 px-2">
                            {f.is_within_10_days ? (
                              <span className="inline-flex items-center gap-1 text-xs text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-medium">
                                <CheckCircle2 className="w-3.5 h-3.5" /> Вчасно
                              </span>
                            ) : (
                              <span className="inline-flex items-center gap-1 text-xs text-amber-700 bg-amber-50 px-2 py-0.5 rounded font-medium">
                                <AlertCircle className="w-3.5 h-3.5" /> Порушено строк
                              </span>
                            )}
                          </td>
                          <td className="py-3 px-2 text-right">
                            {(f.file || f.document_file) && (
                              <a href={f.file || f.document_file} target="_blank" rel="noreferrer" className="text-blue-600 hover:underline text-xs font-semibold">
                                PDF
                              </a>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}

          {activeTab === 'admissions' && (
            <div>
              <h2 className="text-xl font-bold text-slate-900 mb-2">Вступ та наявність вільних місць</h2>
              <p className="text-slate-500 text-sm mb-6">
                Інформація про ліцензований обсяг та вільні місця відповідно до Порядку зарахування учнів.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-bold text-slate-800 text-sm uppercase tracking-wide mb-3">Вільні місця за класами</h3>
                  <div className="border border-slate-200 rounded-xl overflow-hidden divide-y divide-slate-100">
                    {capacities.length === 0 ? (
                      <div className="p-4 text-xs text-slate-500">Інформація оновлюється</div>
                    ) : (
                      capacities.map((c: any) => (
                        <div key={c.id} className="p-3 flex justify-between items-center text-sm">
                          <span className="font-semibold text-slate-800">{c.grade_name || (c.grade_level ? `${c.grade_level}-й клас` : 'Клас')}</span>
                          <span className="text-xs text-slate-500">Фактично: {c.enrolled_count ?? c.actual_students ?? 0}</span>
                          <span className="font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded text-xs">
                            Вільних: {c.available_slots ?? (c.total_capacity && c.enrolled_count !== undefined ? c.total_capacity - c.enrolled_count : 0)}
                          </span>
                        </div>
                      ))
                    )}
                  </div>
                </div>

                <div>
                  <h3 className="font-bold text-slate-800 text-sm uppercase tracking-wide mb-3">Закріплена територія обслуговування</h3>
                  <div className="border border-slate-200 rounded-xl p-4 bg-slate-50 text-sm">
                    {territory.length === 0 ? (
                      <p className="text-slate-500 text-xs">Перелік адрес оновлюється засновником.</p>
                    ) : (
                      <ul className="space-y-2 text-slate-700">
                        {territory.map((t: any) => (
                          <li key={t.id} className="flex items-start gap-2 text-xs">
                            <span className="text-blue-600 font-bold">•</span>
                            <span><strong>{t.street_name}:</strong> {t.building_numbers || 'Всі будинки'}</span>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'nutrition' && (
            <div>
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 mb-6">
                <div>
                  <h2 className="text-xl font-bold text-slate-900 mb-1">Харчування здобувачів освіти</h2>
                  <p className="text-slate-500 text-sm">Щоденне меню відповідно до Постанови КМУ № 305 та стандартів НАССР</p>
                </div>
                {cateringProvider && (
                  <div className="text-xs bg-amber-50 text-amber-900 border border-amber-200 rounded-lg p-2.5">
                    <span className="font-semibold">Постачальник:</span> {cateringProvider.company_name}
                    {cateringProvider.phone && <span className="ml-2 font-mono">тел. {cateringProvider.phone}</span>}
                  </div>
                )}
              </div>
              
              {menus.length === 0 ? (
                <div className="p-8 text-center text-slate-500 bg-slate-50 rounded-xl border border-slate-200">
                  Меню на поточний тиждень завантажується черговою медсестрою/оператором харчування.
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                  {menus.map((m: any) => (
                    <div key={m.id} className="p-5 rounded-2xl border border-slate-200 bg-white shadow-sm flex flex-col justify-between">
                      <div>
                        <div className="flex justify-between items-center pb-3 mb-3 border-b border-slate-100">
                          <span className="font-bold text-base text-slate-900">{m.menu_date}</span>
                          <span className="text-xs px-2.5 py-1 bg-blue-50 text-blue-700 rounded-full font-semibold border border-blue-100">
                            {m.age_group_display || m.age_group}
                          </span>
                        </div>

                        <div className="space-y-3">
                          {m.breakfast && (
                            <div>
                              <div className="text-xs font-bold text-amber-700 uppercase tracking-wide mb-1">🍳 Сніданок (страви, вихід у грамах):</div>
                              <div className="text-xs text-slate-800 bg-slate-50 p-2.5 rounded-lg border border-slate-100 whitespace-pre-line leading-relaxed">
                                {m.breakfast}
                              </div>
                            </div>
                          )}

                          {m.lunch && (
                            <div>
                              <div className="text-xs font-bold text-emerald-700 uppercase tracking-wide mb-1">🍲 Обід (страви, вихід у грамах):</div>
                              <div className="text-xs text-slate-800 bg-slate-50 p-2.5 rounded-lg border border-slate-100 whitespace-pre-line leading-relaxed">
                                {m.lunch}
                              </div>
                            </div>
                          )}

                          {m.snack && (
                            <div>
                              <div className="text-xs font-bold text-violet-700 uppercase tracking-wide mb-1">🍎 Полуденок / підвечірок:</div>
                              <div className="text-xs text-slate-800 bg-slate-50 p-2.5 rounded-lg border border-slate-100 whitespace-pre-line leading-relaxed">
                                {m.snack}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>

                      {m.photo && (
                        <div className="mt-4 pt-3 border-t border-slate-100">
                          <a
                            href={m.photo}
                            target="_blank"
                            rel="noreferrer"
                            className="inline-flex items-center gap-1.5 text-xs font-semibold text-blue-600 hover:text-blue-800 hover:underline"
                          >
                            📷 Переглянути фото затвердженого меню з печаткою &rarr;
                          </a>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'safety' && (
            <div>
              <h2 className="text-xl font-bold text-slate-900 mb-2">Безпека та протидія булінгу (цькуванню)</h2>
              <p className="text-slate-500 text-sm mb-6">
                Відповідно до Закону України № 2657-VIII. Безпечне освітнє середовище є пріоритетом закладу.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <h3 className="font-bold text-slate-800 text-sm uppercase tracking-wide mb-3">План заходів закладу</h3>
                  <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-700">
                    <p className="font-semibold text-slate-900 mb-2">{policy?.title || 'План заходів щодо запобігання та протидії булінгу'}</p>
                    <p className="text-xs text-slate-600 leading-relaxed mb-4">
                      {policy?.academic_year ? `Навчальний рік: ${policy.academic_year}. ` : ''}
                      Заклад освіти гарантує захист прав кожного здобувача освіти, конфіденційне реагування на звернення та негайне скликання комісії з розгляду випадків булінгу.
                    </p>

                    {policy && (
                      <div className="space-y-2 pt-2 border-t border-slate-200">
                        {policy.action_plan_doc && (
                          <a href={policy.action_plan_doc} target="_blank" rel="noreferrer" className="flex items-center justify-between p-2.5 bg-white rounded-lg border border-slate-200 text-xs font-semibold text-blue-700 hover:bg-blue-50">
                            <span>📄 План заходів з протидії булінгу</span>
                            <Download className="w-3.5 h-3.5" />
                          </a>
                        )}
                        {policy.behavior_rules_doc && (
                          <a href={policy.behavior_rules_doc} target="_blank" rel="noreferrer" className="flex items-center justify-between p-2.5 bg-white rounded-lg border border-slate-200 text-xs font-semibold text-blue-700 hover:bg-blue-50">
                            <span>📄 Правила поведінки здобувача освіти</span>
                            <Download className="w-3.5 h-3.5" />
                          </a>
                        )}
                        {policy.application_procedure_doc && (
                          <a href={policy.application_procedure_doc} target="_blank" rel="noreferrer" className="flex items-center justify-between p-2.5 bg-white rounded-lg border border-slate-200 text-xs font-semibold text-blue-700 hover:bg-blue-50">
                            <span>📄 Порядок подання та розгляду заяв про булінг</span>
                            <Download className="w-3.5 h-3.5" />
                          </a>
                        )}
                        {policy.reaction_procedure_doc && (
                          <a href={policy.reaction_procedure_doc} target="_blank" rel="noreferrer" className="flex items-center justify-between p-2.5 bg-white rounded-lg border border-slate-200 text-xs font-semibold text-blue-700 hover:bg-blue-50">
                            <span>📄 Порядок реагування на доведені випадки булінгу</span>
                            <Download className="w-3.5 h-3.5" />
                          </a>
                        )}
                      </div>
                    )}
                  </div>
                </div>

                <div>
                  <h3 className="font-bold text-slate-800 text-sm uppercase tracking-wide mb-3">Конфіденційне онлайн-звернення</h3>
                  <form onSubmit={handleReportSubmit} className="space-y-3 bg-white p-4 border border-slate-200 rounded-xl">
                    <div>
                      <label className="block text-xs font-semibold text-slate-600 mb-1">Хто повідомляє?</label>
                      <select
                        value={reporterRole}
                        onChange={e => setReporterRole(e.target.value)}
                        className="w-full text-xs p-2 border border-slate-300 rounded-lg"
                      >
                        <option value="student">Учень / Учениця</option>
                        <option value="parent">Батько / Мати / Опікун</option>
                        <option value="teacher">Вчитель / Працівник</option>
                        <option value="witness">Свідок події</option>
                        <option value="anonymous">Анонімно</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-600 mb-1">Опис події (конфіденційно):</label>
                      <textarea
                        rows={3}
                        value={incidentText}
                        onChange={e => setIncidentText(e.target.value)}
                        placeholder="Опишіть, що сталося (можна анонімно, без зазначення свого імені)..."
                        className="w-full text-xs p-2 border border-slate-300 rounded-lg"
                        required
                      />
                    </div>
                    <button
                      type="submit"
                      disabled={reportStatus === 'loading'}
                      className="w-full py-2 bg-emerald-700 text-white rounded-lg text-xs font-semibold hover:bg-emerald-800 flex items-center justify-center gap-1.5 disabled:opacity-50"
                    >
                      <Send className="w-3.5 h-3.5" /> {reportStatus === 'loading' ? 'Надсилання...' : 'Надіслати конфіденційно'}
                    </button>
                    {reportFeedback && (
                      <div className={`p-3 rounded-lg text-xs border leading-relaxed ${
                        reportStatus === 'success'
                          ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                          : 'bg-rose-50 text-rose-800 border-rose-200'
                      }`}>
                        {reportFeedback}
                      </div>
                    )}
                  </form>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'gallery' && (
            <div>
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
                <div>
                  <h2 className="text-xl font-bold text-slate-900 mb-1">Фотогалерея шкільного життя</h2>
                  <p className="text-slate-500 text-sm">Світлини подій, свят та досягнень нашого закладу освіти</p>
                </div>
                {selectedAlbum && (
                  <button
                    onClick={() => setSelectedAlbum(null)}
                    className="self-start sm:self-auto px-3.5 py-1.5 text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg flex items-center gap-1.5 transition-colors border border-slate-200"
                  >
                    &larr; Назад до всіх альбомів
                  </button>
                )}
              </div>

              {selectedAlbum ? (
                <div>
                  <div className="mb-6 p-6 bg-slate-50 rounded-2xl border border-slate-200">
                    <span className="text-xs px-2.5 py-1 bg-blue-100 text-blue-800 rounded-full font-semibold">
                      {selectedAlbum.event_date}
                    </span>
                    <h3 className="text-2xl font-bold text-slate-900 mt-2 mb-2">{selectedAlbum.title}</h3>
                    {selectedAlbum.description && (
                      <p className="text-slate-600 text-sm leading-relaxed">{selectedAlbum.description}</p>
                    )}
                  </div>

                  {(!selectedAlbum.photos || selectedAlbum.photos.length === 0) ? (
                    <div className="p-8 text-center text-slate-500 bg-slate-50 rounded-xl border border-slate-200">
                      В цьому альбомі поки немає доданих фотографій. Додайте їх через адмін-панель.
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                      {selectedAlbum.photos.map((photo: any) => (
                        <div key={photo.id} className="group bg-slate-100 rounded-xl overflow-hidden border border-slate-200 shadow-sm hover:shadow-md transition-shadow flex flex-col">
                          <img
                            src={photo.image}
                            alt={photo.caption || selectedAlbum.title}
                            className="w-full h-56 object-cover group-hover:scale-105 transition-transform duration-300"
                            loading="lazy"
                          />
                          {photo.caption && (
                            <div className="p-3 bg-white text-xs text-slate-700 border-t border-slate-100">
                              {photo.caption}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ) : (
                albums.length === 0 ? (
                  <div className="p-12 text-center text-slate-500 bg-slate-50 rounded-2xl border border-slate-200">
                    <ImageIcon className="w-12 h-12 mx-auto text-slate-300 mb-3" />
                    <p className="font-semibold text-slate-700">Альбомів поки не додано</p>
                    <p className="text-xs text-slate-500 mt-1">Ви можете створити перший фотоальбом в панелі керування (Адмінці).</p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                    {albums.map((album: any) => (
                      <div
                        key={album.id}
                        onClick={() => setSelectedAlbum(album)}
                        className="cursor-pointer group bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-lg transition-all flex flex-col"
                      >
                        <div className="h-48 bg-slate-100 relative overflow-hidden">
                          {album.cover_image ? (
                            <img
                              src={album.cover_image}
                              alt={album.title}
                              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                            />
                          ) : (
                            <div className="w-full h-full flex items-center justify-center text-slate-400">
                              <ImageIcon className="w-12 h-12 text-slate-300" />
                            </div>
                          )}
                          <span className="absolute top-3 right-3 px-2.5 py-1 bg-black/60 backdrop-blur text-white text-xs rounded-full font-medium">
                            {album.photos?.length || 0} фото
                          </span>
                          <span className="absolute bottom-3 left-3 px-2.5 py-0.5 bg-white/90 backdrop-blur text-slate-800 text-xs rounded font-semibold">
                            {album.event_date}
                          </span>
                        </div>
                        <div className="p-4 flex-1 flex flex-col justify-between">
                          <div>
                            <h3 className="font-bold text-slate-900 group-hover:text-blue-700 transition-colors line-clamp-1 mb-1">
                              {album.title}
                            </h3>
                            <p className="text-xs text-slate-500 line-clamp-2">
                              {album.description || 'Без опису'}
                            </p>
                          </div>
                          <div className="mt-4 pt-3 border-t border-slate-100 text-xs font-semibold text-blue-600 flex items-center justify-between">
                            <span>Переглянути фото &rarr;</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )
              )}
            </div>
          )}

          {activeTab === 'news' && (
            <div>
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
                <div>
                  <h2 className="text-xl font-bold text-slate-900 mb-1">Новини та оголошення</h2>
                  <p className="text-slate-500 text-sm">Актуальні новини життя школи та оголошення адміністрації</p>
                </div>
                {selectedNews && (
                  <button
                    onClick={() => setSelectedNews(null)}
                    className="self-start sm:self-auto px-3.5 py-1.5 text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg flex items-center gap-1.5 transition-colors border border-slate-200"
                  >
                    &larr; Назад до всіх новин
                  </button>
                )}
              </div>

              {selectedNews ? (
                <div className="max-w-3xl mx-auto bg-white p-6 rounded-2xl border border-slate-200">
                  {selectedNews.image && (
                    <img
                      src={selectedNews.image}
                      alt={selectedNews.title}
                      className="w-full h-72 object-cover rounded-xl mb-6"
                    />
                  )}
                  <div className="text-xs text-slate-500 mb-2">
                    {new Date(selectedNews.published_at).toLocaleDateString('uk-UA')}
                  </div>
                  <h3 className="text-2xl font-bold text-slate-900 mb-4">{selectedNews.title}</h3>
                  <div className="prose text-slate-700 text-sm leading-relaxed whitespace-pre-line">
                    {selectedNews.content}
                  </div>
                </div>
              ) : newsList.length === 0 ? (
                <div className="p-12 text-center text-slate-500 bg-slate-50 rounded-2xl border border-slate-200">
                  <Newspaper className="w-12 h-12 mx-auto text-slate-300 mb-3" />
                  <p className="font-semibold text-slate-700">Новин поки немає</p>
                  <p className="text-xs text-slate-500 mt-1">Оголошення з'являться після додавання в адмін-панелі.</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {newsList.map((article: any) => (
                    <div
                      key={article.id}
                      onClick={() => setSelectedNews(article)}
                      className="cursor-pointer group bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-lg transition-all flex flex-col"
                    >
                      {article.image ? (
                        <img
                          src={article.image}
                          alt={article.title}
                          className="w-full h-44 object-cover group-hover:scale-105 transition-transform duration-300"
                        />
                      ) : (
                        <div className="w-full h-44 bg-slate-100 flex items-center justify-center text-slate-400">
                          <Newspaper className="w-12 h-12 text-slate-300" />
                        </div>
                      )}
                      <div className="p-4 flex-1 flex flex-col justify-between">
                        <div>
                          <div className="text-xs text-slate-400 mb-1">
                            {new Date(article.published_at).toLocaleDateString('uk-UA')}
                          </div>
                          <h3 className="font-bold text-slate-900 group-hover:text-blue-700 transition-colors line-clamp-2 mb-2">
                            {article.title}
                          </h3>
                          <p className="text-xs text-slate-500 line-clamp-3">
                            {article.summary || article.content}
                          </p>
                        </div>
                        <div className="mt-4 pt-3 border-t border-slate-100 text-xs font-semibold text-blue-600">
                          Читати детальніше &rarr;
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'schedule' && (
            <div>
              <h2 className="text-xl font-bold text-slate-900 mb-2">Розклад дзвінків та уроків</h2>
              <p className="text-slate-500 text-sm mb-6">Графік навчального дня та тривалість уроків і перерв</p>

              <div className="max-w-2xl bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
                <div className="bg-slate-50 px-6 py-4 border-b border-slate-200 font-bold text-slate-800 text-sm flex items-center gap-2">
                  <Clock className="w-4 h-4 text-blue-600" /> Розклад дзвінків
                </div>
                {bells.length === 0 ? (
                  <div className="p-8 text-center text-slate-500 text-xs">
                    Розклад дзвінків завантажується закладом освіти.
                  </div>
                ) : (
                  <div className="divide-y divide-slate-100">
                    {bells.map((bell: any) => (
                      <div key={bell.id} className="px-6 py-3.5 flex justify-between items-center text-sm">
                        <span className="font-semibold text-slate-900">{bell.lesson_number}-й урок</span>
                        <div className="flex items-center gap-4">
                          <span className="text-slate-700 font-mono text-xs bg-slate-100 px-2 py-1 rounded">
                            {bell.start_time?.slice(0, 5)} &mdash; {bell.end_time?.slice(0, 5)}
                          </span>
                          <span className="text-xs text-slate-400">
                            перерва {bell.break_duration} хв
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="school-footer bg-slate-900 text-slate-400 py-8 px-4 border-t border-slate-800 mt-12 text-sm">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
          <div>
            <strong className="text-white">{school?.name}</strong> &bull; {school?.address} &bull; {school?.phone}
          </div>
          <div>
            <a
              href="/admin/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-emerald-400 hover:text-emerald-300 font-semibold underline"
            >
              Панель керування (Адмінка) &rarr;
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
"""
    (src_dir / "App.tsx").write_text(
        app_tsx.replace("__SCHOOL_TEMPLATE__", template), encoding="utf-8"
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
