from django.db import models
from django.utils.translation import gettext_lazy as _

class AntiBullyingPolicy(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Назва політики / наказу'))
    academic_year = models.CharField(max_length=50, verbose_name=_('Навчальний рік (наприклад: 2026/2027)'))
    behavior_rules_doc = models.FileField(
        upload_to='safety/rules/',
        verbose_name=_('Правила поведінки здобувача освіти в закладі')
    )
    application_procedure_doc = models.FileField(
        upload_to='safety/procedures/',
        verbose_name=_('Порядок подання та розгляду заяв про випадки булінгу (з конфіденційністю)')
    )
    reaction_procedure_doc = models.FileField(
        upload_to='safety/procedures/',
        verbose_name=_('Порядок реагування на доведені випадки булінгу та відповідальність')
    )
    action_plan_doc = models.FileField(
        upload_to='safety/plans/',
        verbose_name=_('План заходів щодо запобігання та протидії булінгу')
    )
    is_active = models.BooleanField(default=True, verbose_name=_('Чинна редакція'))

    class Meta:
        verbose_name = _('Політика та план протидії булінгу')
        verbose_name_plural = _('Політики та плани протидії булінгу')

    def __str__(self):
        return f"{self.title} ({self.academic_year})"


class ConfidentialReport(models.Model):
    REPORTER_ROLES = [
        ('student', _('Учень / учениця')),
        ('parent', _('Батьки / законні представники')),
        ('teacher', _('Педагогічний працівник')),
        ('anonymous', _('Анонімно')),
    ]

    reporter_role = models.CharField(max_length=20, choices=REPORTER_ROLES, default='anonymous', verbose_name=_('Статус заявника'))
    incident_description = models.TextField(verbose_name=_('Опис фактів та обставин випадку булінгу'))
    contact_feedback = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Контакт для зворотного зв’язку (email або телефон, за бажанням)')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата та час надсилання'))
    is_reviewed = models.BooleanField(default=False, verbose_name=_('Опрацьовано комісією закладу'))
    review_notes = models.TextField(blank=True, verbose_name=_('Службові примітки комісії'))

    class Meta:
        verbose_name = _('Конфіденційне звернення про булінг')
        verbose_name_plural = _('Конфіденційні звернення про булінг (конфіденційно)')
        ordering = ['-created_at']

    def __str__(self):
        return f"Звернення #{self.id} ({self.get_reporter_role_display()}) від {self.created_at.strftime('%d.%m.%Y')}"
