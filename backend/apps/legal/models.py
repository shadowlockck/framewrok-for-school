from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

class LegalDocumentCategory(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Категорія документа'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('Порядок відображення'))

    class Meta:
        verbose_name = _('Категорія нормативних документів')
        verbose_name_plural = _('Категорії нормативних документів')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class LegalDocument(models.Model):
    category = models.ForeignKey(
        LegalDocumentCategory,
        on_delete=models.PROTECT,
        related_name='documents',
        verbose_name=_('Категорія')
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_('Назва документа')
    )
    law_reference = models.CharField(
        max_length=150,
        default='ст. 30 ЗУ «Про освіту»',
        verbose_name=_('Норма закону')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Короткий зміст або опис')
    )
    file = models.FileField(
        upload_to='legal/documents/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_('Файл документа (PDF/DOCX)')
    )
    external_url = models.URLField(
        blank=True,
        verbose_name=_('Посилання на сайт засновника / реєстр (якщо документ розміщено зовні)')
    )
    approval_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Дата затвердження')
    )
    publish_date = models.DateField(
        auto_now_add=True,
        verbose_name=_('Дата оприлюднення')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Чинний документ')
    )

    class Meta:
        verbose_name = _('Обов’язковий нормативний документ')
        verbose_name_plural = _('Обов’язкові нормативні документи (ст. 30)')
        ordering = ['category', '-publish_date']

    def __str__(self):
        return self.title


class FinancialReport(models.Model):
    REPORT_TYPES = [
        ('estimate', _('Кошторис закладу')),
        ('quarterly_report', _('Квартальний / річний фінансовий звіт')),
        ('charity', _('Благодійна допомога (товари, роботи, послуги)')),
        ('other', _('Інші джерела надходжень')),
    ]

    title = models.CharField(max_length=255, verbose_name=_('Назва звіту / кошторису'))
    report_type = models.CharField(max_length=30, choices=REPORT_TYPES, default='estimate', verbose_name=_('Тип звітності'))
    period = models.CharField(max_length=50, verbose_name=_('Звітний період (рік або квартал)'))
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, verbose_name=_('Сума коштів (грн)'))
    approval_date = models.DateField(verbose_name=_('Дата затвердження'))
    publish_date = models.DateField(verbose_name=_('Дата оприлюднення на сайті'))
    file = models.FileField(upload_to='legal/finance/%Y/', verbose_name=_('Файл звітності'))
    notes = models.TextField(blank=True, verbose_name=_('Примітки / деталізація'))

    class Meta:
        verbose_name = _('Фінансова звітність та кошторис')
        verbose_name_plural = _('Фінансова звітність та кошториси (п. 3 ст. 30)')
        ordering = ['-publish_date']

    def __str__(self):
        return f"{self.title} ({self.period})"

    @property
    def is_within_10_days(self):
        """Перевірка чи документ оприлюднено в межах 10 днів від затвердження"""
        if self.approval_date and self.publish_date:
            return (self.publish_date - self.approval_date) <= timedelta(days=14)
        return True


class StaffMember(models.Model):
    full_name = models.CharField(max_length=150, verbose_name=_('ПІБ працівника'))
    position = models.CharField(max_length=150, verbose_name=_('Посада'))
    is_administration = models.BooleanField(default=False, verbose_name=_('Керівний склад / Адміністрація'))
    category = models.CharField(max_length=100, blank=True, verbose_name=_('Кваліфікаційна категорія'))
    pedagogical_title = models.CharField(max_length=100, blank=True, verbose_name=_('Педагогічне звання'))
    education = models.CharField(max_length=255, blank=True, verbose_name=_('Освіта / навчальний заклад'))
    last_qualification_update = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Рік останнього підвищення кваліфікації'))
    photo = models.ImageField(upload_to='staff/', blank=True, null=True, verbose_name=_('Фото'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('Порядок сортування'))

    class Meta:
        verbose_name = _('Працівник кадрового складу')
        verbose_name_plural = _('Кадровий склад згідно з ліцензійними умовами')
        ordering = ['-is_administration', 'order', 'full_name']

    def __str__(self):
        return f"{self.full_name} — {self.position}"


class Vacancy(models.Model):
    position_title = models.CharField(max_length=200, verbose_name=_('Вакантна посада'))
    salary_conditions = models.CharField(max_length=255, blank=True, verbose_name=_('Умови оплати праці'))
    requirements = models.TextField(verbose_name=_('Кваліфікаційні вимоги'))
    is_director_vacancy = models.BooleanField(
        default=False,
        verbose_name=_('Конкурс на посаду керівника закладу (ст. 39 ЗУ «Про повну загальну середню освіту»)')
    )
    application_deadline = models.DateTimeField(verbose_name=_('Кінцевий строк подання документів'))
    contact_person = models.CharField(max_length=255, verbose_name=_('Уповноважена особа (ПІБ, телефон, email)'))
    is_open = models.BooleanField(default=True, verbose_name=_('Прийом документів триває'))

    class Meta:
        verbose_name = _('Вакантна посада / конкурс')
        verbose_name_plural = _('Вакансії та конкурси')
        ordering = ['-is_open', 'application_deadline']

    def __str__(self):
        return f"Вакансія: {self.position_title}"
