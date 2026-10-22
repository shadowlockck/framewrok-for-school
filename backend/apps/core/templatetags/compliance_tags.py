from django import template
from django.apps import apps
from django.contrib import admin
from django.urls import reverse
from apps.core.compliance import ComplianceAuditor

register = template.Library()


AUDIT_MODELS = {
    'profile': 'core.SchoolProfile',
    'language': 'core.SchoolProfile',
    'capacity_stats': 'core.SchoolProfile',
    'charter': 'legal.LegalDocument',
    'license': 'legal.LegalDocument',
    'accreditation': 'legal.LegalDocument',
    'structure': 'legal.LegalDocument',
    'staff': 'legal.StaffMember',
    'annual_report': 'legal.LegalDocument',
    'finance_reports': 'legal.FinancialReport',
    'territory': 'admissions.ServiceTerritory',
    'class_capacity': 'admissions.ClassCapacity',
    'bullying_policy': 'safety.AntiBullyingPolicy',
    'daily_menu': 'nutrition.DailyMenu',
}


@register.simple_tag(takes_context=True)
def get_compliance_report(context):
    """
    Повертає аудит-звіт відповідності закладу освіти вимогам
    ст. 30 ЗУ «Про освіту» та суміжного законодавства.
    """
    report = ComplianceAuditor.get_audit_report()
    request = context.get('request')
    checks = []
    for check in report['checks']:
        visible = {**check, 'admin_url': None}
        label = AUDIT_MODELS.get(check['code'])
        if request is not None and label and apps.is_installed(f'apps.{label.split(".")[0]}'):
            model = apps.get_model(label)
            if admin.site.is_registered(model):
                model_admin = admin.site.get_model_admin(model)
                if model_admin.has_view_permission(request) or model_admin.has_change_permission(request):
                    visible['admin_url'] = reverse(
                        f'admin:{model._meta.app_label}_{model._meta.model_name}_changelist'
                    )
        checks.append(visible)
    return {**report, 'checks': checks}
