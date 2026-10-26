# Django School Framework

Фреймворк для створення сайтів закладів освіти України: Django API, панель адміністратора, редакторські ролі та генератор React-фронтенду. Поточна версія вихідного коду — **0.2.8** (Python 3.11+, Django 5.2). [Документація](http://4.165.133.94/) · [PyPI](https://pypi.org/project/django-school-framework/) · [Лендінг](http://4.165.133.94/landing/).

## Можливості

- Модулі `core`, `legal`, `admissions`, `nutrition`, `safety`, `news`, `schedule`, `gallery`; їх можна вмикати окремо. `schedule` потребує `admissions`.
- REST API та OpenAPI, профіль закладу, маніфест активних модулів за `/api/v1/core/manifest/`.
- Django Admin із ролями для редакторів окремих розділів. Редактор може публікувати матеріали свого розділу; права перевіряються на сервері. [Матриця ролей](docs/editor-roles.md).
- `school-admin` створює Django-проєкт і, за потреби, React-сайт у макеті `classic`, `editorial` або `portal`.
- `school-admin check-compliance` показує заповненість полів і документів, які перевіряє програма. Це **не юридичний висновок** і не гарантія відповідності [статті 30 Закону України «Про освіту»](https://zakon.rada.gov.ua/laws/show/2145-19#Text). Вміст, строки публікації, персональні дані та доступність сайту потрібно перевіряти окремо.

## Створити сайт із пакета

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade django-school-framework
school-admin startproject my_school --frontend-template classic
cd my_school
python manage.py migrate
python manage.py setup_school_roles
python manage.py createsuperuser
school-admin create-school "Гімназія №1" --edrpou 12345678
python manage.py runserver
```

У другому терміналі, із каталогу `my_school`:

```bash
cd frontend
npm install
npm run dev
```

Сайт відкривається на `http://localhost:5173/`, Django Admin — на `http://127.0.0.1:8000/admin/`, OpenAPI — на `http://127.0.0.1:8000/api/docs/`. Якщо Vite вибрав інший порт, використовуйте адресу з його виводу. Для іншого дизайну замініть `classic` на `editorial` або `portal`. Без `--frontend-template` команда створить тільки Django-проєкт; додати сайт згодом можна через `school-admin create-frontend --template portal`.

`.env.example` є зразком: Django **не зчитує `.env` автоматично**. Передайте змінні через оболонку, менеджер процесів або налаштуйте завантаження `.env` у своєму проєкті. Локально генератор використовує SQLite; для сервера налаштуйте відповідну СУБД і збережіть облікові дані поза Git. Для продакшену задайте `DEBUG=False`, `DJANGO_SECRET_KEY`, `ALLOWED_HOSTS`, HTTPS та виконайте `python manage.py check --deploy`. Див. [посібник із розгортання](docs/deployment-guide.md).

Команда `school-admin seed-data` створює **демонстраційні** записи; не публікуйте їх як документи реального закладу. Після заповнення сайту `school-admin check-compliance` допоможе знайти відсутні дані.

## Розробка в цьому репозиторії

У корені лежать `backend/` (пакет Django), `frontend/` (UI-бібліотека та приклад), `docs/` (технічні інструкції). Окремий сайт документації зібраний з [MkDocs-проєкту](http://4.165.133.94/). Для запуску наявного монорепозиторію через Docker Compose:

```bash
cp .env.example .env
docker compose up -d --build
```

Цей Compose-файл призначений для **локальної розробки**: MySQL 8, Django `runserver` і Vite. Змініть паролі в `.env`; не використовуйте його без додаткового захисту як готову production-конфігурацію. Адмінка працює на `http://localhost:8000/admin/`.

Перевірки:

```bash
PYTHONPATH=backend ./venv/bin/python backend/manage.py test apps.core apps.legal apps.admissions apps.nutrition apps.safety apps.news apps.schedule apps.gallery
cd frontend && npm run build
```

Для перевірки встановленого пакета та генератора використовуйте `python scripts/smoke_installed_package.py`; скрипту потрібні Python із `setuptools` і `wheel`, Node.js/npm та доступ до мережі. [Архітектура](docs/framework-architecture.md) · [Ліцензія MIT](LICENSE).
