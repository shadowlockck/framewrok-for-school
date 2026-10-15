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
    # ...
    'apps.core',
    'apps.legal',
    'apps.admissions',
    'apps.nutrition',
    'apps.safety',
    'apps.news',
    'apps.schedule',
    'apps.gallery',
]
```
