from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .modules import installed_modules, module_navigation
from .models import SchoolProfile, ThemeSettings
from .serializers import (
    ComplianceReportSerializer,
    SchoolManifestSerializer,
    SchoolProfileSerializer,
    ThemeSettingsSerializer,
)

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

    @extend_schema(responses=SchoolManifestSerializer)
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

        modules = installed_modules()
        navigation = module_navigation(modules)

        return Response({
            'school': school_data,
            'modules': modules,
            'navigation': navigation,
            'compliance': {
                'article_30': modules['legal'],
                'wcag_version': '2.1 AA',
                'privacy_law_enforced': True,
                'financial_deadline_days': 10
            }
        })


from .compliance import ComplianceAuditor

class ComplianceAuditView(APIView):
    """
    API монітора інформаційної відкритості закладу освіти:
    Повертає деталізований звіт відповідності вимогам ст. 30 ЗУ «Про освіту»,
    відсоток виконання та оперативні попередження щодо строків.
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(responses=ComplianceReportSerializer)
    def get(self, request, *args, **kwargs):
        report = ComplianceAuditor.get_audit_report()
        return Response(report)


from django.views.generic import TemplateView

class PublicSchoolHomeView(TemplateView):
    """
    Публічна головна сторінка закладу освіти з підтримкою доступності WCAG 2.1 AA
    та автоматичним відображенням статусу ст. 30 ЗУ «Про освіту».
    """
    template_name = 'school/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['school'] = SchoolProfile.objects.select_related('theme').first()
        ctx['modules'] = installed_modules()
        ctx['compliance'] = ComplianceAuditor.get_audit_report()
        return ctx


