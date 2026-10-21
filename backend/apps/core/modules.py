"""The built-in module contract shared by generated and source projects."""

from django.apps import apps
from django.core.checks import Error, register
from django.urls import include, path


MODULES = {
    'legal': {
        'navigation': [
            {'id': 'legal', 'title': 'Прозорість (ст. 30)', 'icon': 'FileCheck'},
            {'id': 'finance', 'title': 'Кошторис та звітність', 'icon': 'DollarSign'},
        ],
    },
    'admissions': {'navigation': [{'id': 'admissions', 'title': 'Вступ та зарахування', 'icon': 'Users'}]},
    'nutrition': {'navigation': [{'id': 'nutrition', 'title': 'Харчування', 'icon': 'Utensils'}]},
    'safety': {'navigation': [{'id': 'safety', 'title': 'Безпека та булінг', 'icon': 'ShieldAlert'}]},
    'news': {'navigation': [{'id': 'news', 'title': 'Новини', 'icon': 'Newspaper'}]},
    'schedule': {
        'requires': ('admissions',),
        'navigation': [{'id': 'schedule', 'title': 'Розклад', 'icon': 'Calendar'}],
    },
    'gallery': {'navigation': [{'id': 'gallery', 'title': 'Галерея', 'icon': 'Image'}]},
}

# Keep the historical order in the public manifest.
NAVIGATION_ORDER = ('legal', 'admissions', 'schedule', 'nutrition', 'safety', 'news', 'gallery')


def installed_modules():
    return {name: apps.is_installed(f'apps.{name}') for name in MODULES}


def module_navigation(enabled=None):
    enabled = installed_modules() if enabled is None else enabled
    return [item for name in NAVIGATION_ORDER if enabled[name] for item in MODULES[name]['navigation']]


def module_urlpatterns():
    enabled = installed_modules()
    return [
        path(f'api/v1/{name}/', include(f'apps.{name}.urls'))
        for name in MODULES if enabled[name]
    ]


@register()
def check_module_dependencies(app_configs, **kwargs):
    enabled = installed_modules()
    return [
        Error(
            f'Mодуль {name} потребує apps.{dependency}; додайте його до INSTALLED_APPS або вимкніть apps.{name}.',
            id='school.E001',
        )
        for name, config in MODULES.items() if enabled[name]
        for dependency in config.get('requires', ()) if not enabled[dependency]
    ]
