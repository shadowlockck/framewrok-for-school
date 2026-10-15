from django import template
from apps.core.compliance import ComplianceAuditor

register = template.Library()


@register.simple_tag
def get_compliance_report():
    """
    Повертає аудит-звіт відповідності закладу освіти вимогам
    ст. 30 ЗУ «Про освіту» та суміжного законодавства.
    """
    return ComplianceAuditor.get_audit_report()
