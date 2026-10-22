# Django School Framework

Модульний веб-фреймворк для офіційних сайтів закладів загальної середньої освіти України відповідно до ст. 30 ЗУ «Про освіту».

## Встановлення

```bash
pip install django-school-framework
```

## Швидкий старт

Додайте необхідні додатки у ваш `settings.py`:

```python
INSTALLED_APPS = [
    # Перед django.contrib.admin для власного Compliance Dashboard
    'apps.core',
    # ...
    'apps.legal',
    'apps.admissions',
    'apps.nutrition',
    'apps.safety',
    'apps.news',
    'apps.schedule',
    'apps.gallery',
]
```

Після `python manage.py migrate` виконайте `python manage.py setup_school_roles`.
Команда створить групи редакторів для активних модулів. Для попереднього перегляду
використайте `--dry-run`. Дайте працівнику `is_staff` та призначте групи через
Django Admin. Після зміни складу модулів повторіть команду. Подробиці:
[Ролі редакторів](../docs/editor-roles.md).
