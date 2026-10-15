from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.apps import apps
from .models import SchoolProfile, ThemeSettings
from .serializers import SchoolProfileSerializer, ThemeSettingsSerializer

class SchoolProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SchoolProfile.objects.all().select_related('theme')
    serializer_class = SchoolProfileSerializer
    permission_classes = [permissions.AllowAny]


class ThemeSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ThemeSettings.objects.all()
    serializer_class = ThemeSettingsSerializer
    permission_classes = [permissions.AllowAny]


class SchoolManifestView(APIView):
    """
    Системний маніфест закладу освіти для фреймворку:
    Повертає профіль школи, динамічний перелік активних модулів та меню навігації.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        profile = SchoolProfile.objects.select_related('theme').first()
        school_data = SchoolProfileSerializer(profile).data if profile else {
            "name": "Офіційний вебсайт закладу освіти",
            "short_name": "Заклад освіти",
            "edrpou": "",
            "founder": "Орган місцевого самоврядування",
            "address": "",
            "phone": "",
            "email": "",
            "website": "",
            "licensed_capacity": 0,
            "actual_students": 0,
            "education_language": "Українська",
            "logo": None,
            "theme": {
                "primary_color": "#1e3a8a",
                "primary_hover": "#172554",
                "secondary_color": "#059669",
                "accent_color": "#d97706",
                "font_family": "Inter, system-ui, sans-serif"
            }
        }

        # Dynamic module detection based on INSTALLED_APPS
        has_legal = apps.is_installed('apps.legal')
        has_admissions = apps.is_installed('apps.admissions')
        has_nutrition = apps.is_installed('apps.nutrition')
        has_safety = apps.is_installed('apps.safety')
        has_news = apps.is_installed('apps.news')
        has_schedule = apps.is_installed('apps.schedule')
        has_gallery = apps.is_installed('apps.gallery')

        modules = {
            'legal': has_legal,
            'admissions': has_admissions,
            'nutrition': has_nutrition,
            'safety': has_safety,
            'news': has_news,
            'schedule': has_schedule,
            'gallery': has_gallery,
        }

        navigation = []
        if has_legal:
            navigation.append({'id': 'legal', 'title': 'Прозорість (ст. 30)', 'icon': 'FileCheck'})
            navigation.append({'id': 'finance', 'title': 'Кошторис та звітність', 'icon': 'DollarSign'})
        if has_admissions:
            navigation.append({'id': 'admissions', 'title': 'Вступ та зарахування', 'icon': 'Users'})
        if has_schedule:
            navigation.append({'id': 'schedule', 'title': 'Розклад', 'icon': 'Calendar'})
        if has_nutrition:
            navigation.append({'id': 'nutrition', 'title': 'Харчування', 'icon': 'Utensils'})
        if has_safety:
            navigation.append({'id': 'safety', 'title': 'Безпека та булінг', 'icon': 'ShieldAlert'})
        if has_news:
            navigation.append({'id': 'news', 'title': 'Новини', 'icon': 'Newspaper'})
        if has_gallery:
            navigation.append({'id': 'gallery', 'title': 'Галерея', 'icon': 'Image'})

        return Response({
            'school': school_data,
            'modules': modules,
            'navigation': navigation,
            'compliance': {
                'article_30': True,
                'wcag_version': '2.1 AA',
                'privacy_law_enforced': True,
                'financial_deadline_days': 10
            }
        })
