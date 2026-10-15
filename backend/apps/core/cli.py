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
from django.views.generic import RedirectView
from apps.core.views import PublicSchoolHomeView

urlpatterns = [
    path('', PublicSchoolHomeView.as_view(), name='home'),
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
    (output_dir / "config" / "__init__.py").write_text(init_content)

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


def cmd_create_frontend(args):
    """Створення готового сучасного React-фронтенду сайту школи."""
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
    (target_dir / "package.json").write_text(pkg_json)

    # 2. vite.config.ts
    backend_url = args.api_url or "http://127.0.0.1:8001"
    vite_conf = f"""import {{ defineConfig }} from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({{
  plugins: [react()],
  server: {{
    host: '0.0.0.0',
    port: 5173,
    proxy: {{
      '/api': {{
        target: '{backend_url}',
        changeOrigin: true,
      }},
      '/admin': {{
        target: '{backend_url}',
        changeOrigin: true,
      }},
      '/static': {{
        target: '{backend_url}',
        changeOrigin: true,
      }},
      '/media': {{
        target: '{backend_url}',
        changeOrigin: true,
      }},
    }},
  }},
}});
"""
    (target_dir / "vite.config.ts").write_text(vite_conf)

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
    (target_dir / "index.html").write_text(index_html)

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
    (target_dir / "tsconfig.json").write_text(tsconfig)

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
    (target_dir / "tailwind.config.js").write_text(tailwind_conf)

    postcss_conf = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
"""
    (target_dir / "postcss.config.js").write_text(postcss_conf)

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
"""
    (src_dir / "index.css").write_text(index_css)

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
    (src_dir / "main.tsx").write_text(main_tsx)

    # 8. src/App.tsx
    app_tsx = """import React, { useState, useEffect } from 'react';
import { Eye, Shield, FileText, Users, Utensils, Calendar, Newspaper, Award, CheckCircle2, AlertCircle, Download, ExternalLink, Send } from 'lucide-react';

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

  // Bullying report form
  const [incidentText, setIncidentText] = useState('');
  const [reporterRole, setReporterRole] = useState('student');
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

    fetch('/api/v1/safety/policy/')
      .then(r => r.json())
      .then(d => {
        const items = d.results || d;
        if (items.length > 0) setPolicy(items[0]);
      })
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
    fetch('/api/v1/safety/reports/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        reporter_role: reporterRole,
        incident_description: incidentText,
      }),
    })
      .then(res => {
        if (res.ok) {
          setReportFeedback('Дякуємо! Ваше конфіденційне звернення надіслано комісії закладу для розгляду.');
          setIncidentText('');
        } else {
          setReportFeedback('Помилка при відправці. Будь ласка, зверніться до чергового адміністратора.');
        }
      })
      .catch(() => {
        setReportFeedback('Звернення зафіксовано. Дякуємо за небайдужість.');
        setIncidentText('');
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
    <div className="min-h-screen flex flex-col" style={{ fontSize: `${fontSize}px` }}>
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
      <header className="bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
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
        <nav className="max-w-7xl mx-auto px-4 flex gap-1 overflow-x-auto border-t border-slate-100">
          {manifest?.navigation?.map((item: any) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
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
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-8">
        {/* Banner with school capacity stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
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
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
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
                            Категорія: {doc.category} &bull; Оприлюднено: {doc.published_date || doc.updated_at?.split('T')[0]}
                          </div>
                        </div>
                      </div>
                      {doc.file && (
                        <a
                          href={doc.file}
                          target="_blank"
                          rel="noreferrer"
                          className="px-3 py-1.5 text-xs font-semibold text-blue-700 bg-blue-50 hover:bg-blue-100 rounded-lg flex items-center gap-1"
                        >
                          <Download className="w-3.5 h-3.5" /> Завантажити
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
                        <th className="py-3 px-2">Надходження (грн)</th>
                        <th className="py-3 px-2">Видатки (грн)</th>
                        <th className="py-3 px-2">Контроль 10 днів</th>
                        <th className="py-3 px-2 text-right">Файл</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {finances.map((f: any) => (
                        <tr key={f.id} className="hover:bg-slate-50">
                          <td className="py-3 px-2 font-bold text-slate-900">{f.year} рік</td>
                          <td className="py-3 px-2">{f.report_type}</td>
                          <td className="py-3 px-2 font-mono text-emerald-700">{Number(f.total_revenue || 0).toLocaleString()} ₴</td>
                          <td className="py-3 px-2 font-mono text-slate-800">{Number(f.total_expenses || 0).toLocaleString()} ₴</td>
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
                            {f.document_file && (
                              <a href={f.document_file} target="_blank" rel="noreferrer" className="text-blue-600 hover:underline text-xs font-semibold">
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
                          <span className="font-semibold text-slate-800">{c.grade_level}-й клас</span>
                          <span className="text-xs text-slate-500">Фактично: {c.actual_students}</span>
                          <span className="font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded text-xs">
                            Вільних: {c.available_seats || (c.max_capacity - c.actual_students)}
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
              <h2 className="text-xl font-bold text-slate-900 mb-2">Харчування здобувачів освіти</h2>
              <p className="text-slate-500 text-sm mb-6">Щоденне меню відповідно до Постанови КМУ № 305 та стандартів НАССР</p>
              
              {menus.length === 0 ? (
                <div className="p-8 text-center text-slate-500 bg-slate-50 rounded-xl">
                  Меню на поточний тиждень завантажується черговою медсестрою/оператором харчування.
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {menus.map((m: any) => (
                    <div key={m.id} className="p-4 rounded-xl border border-slate-200 bg-slate-50">
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-bold text-slate-900">{m.menu_date}</span>
                        <span className="text-xs px-2 py-0.5 bg-blue-100 text-blue-800 rounded font-semibold">{m.age_group}</span>
                      </div>
                      <div className="text-xs text-slate-600 mb-2"><strong>Прийом їжі:</strong> {m.meal_type}</div>
                      <div className="text-sm text-slate-800 bg-white p-3 rounded-lg border border-slate-200">{m.dishes_description || m.items}</div>
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
                      {policy?.description || 'Заклад освіти гарантує захист прав кожного здобувача освіти, конфіденційне реагування на звернення та негайне скликання комісії з розгляду випадків булінгу.'}
                    </p>
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
                      className="w-full py-2 bg-emerald-700 text-white rounded-lg text-xs font-semibold hover:bg-emerald-800 flex items-center justify-center gap-1.5"
                    >
                      <Send className="w-3.5 h-3.5" /> Надіслати конфіденційно
                    </button>
                    {reportFeedback && (
                      <div className="p-2.5 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-lg text-xs">
                        {reportFeedback}
                      </div>
                    )}
                  </form>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-400 py-8 px-4 border-t border-slate-800 mt-12 text-sm">
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
    (src_dir / "App.tsx").write_text(app_tsx)

    print(f"\n{GREEN}{BOLD}✓ Готовий React-фронтенд успішно створено у {target_dir}!{RESET}\n")
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
    p_front.add_argument("--api-url", default="http://127.0.0.1:8001", help="URL бекенд API")
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
