from django.db import models
from django.utils.translation import gettext_lazy as _

class SchoolProfile(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Повна назва закладу освіти'),
        help_text=_('Наприклад: Ліцей "Інтелект та Інновації" Київської міської ради')
    )
    short_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Скорочена назва')
    )
    edrpou = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_('Код ЄДРПОУ')
    )
    founder = models.CharField(
        max_length=255,
        verbose_name=_('Засновник закладу освіти'),
        help_text=_('Орган державної влади, відповідна рада територіальної громади або уповноважена особа')
    )
    address = models.CharField(
        max_length=255,
        verbose_name=_('Місцезнаходження (юридична адреса)')
    )
    phone = models.CharField(
        max_length=50,
        verbose_name=_('Контактний телефон')
    )
    email = models.EmailField(
        verbose_name=_('Офіційна електронна адреса')
    )
    website = models.URLField(
        blank=True,
        verbose_name=_('Адреса веб-сайту')
    )
    licensed_capacity = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Ліцензований обсяг (кількість учнів)')
    )
    actual_students = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Фактична кількість здобувачів освіти')
    )
    education_language = models.CharField(
        max_length=100,
        default='Українська',
        verbose_name=_('Мова (мови) освітнього процесу')
    )
    logo = models.ImageField(
        upload_to='school/logo/',
        blank=True,
        null=True,
        verbose_name=_('Логотип / герб закладу')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Профіль закладу освіти')
        verbose_name_plural = _('Профіль закладу освіти')
        ordering = ['id']

    def __str__(self):
        return f"{self.name} (ЄДРПОУ {self.edrpou})"


class ThemeSettings(models.Model):
    school = models.OneToOneField(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name='theme',
        verbose_name=_('Заклад освіти')
    )
    primary_color = models.CharField(
        max_length=20,
        default='#1e3a8a',
        verbose_name=_('Основний колір (Primary Hex)')
    )
    primary_hover = models.CharField(
        max_length=20,
        default='#172554',
        verbose_name=_('Колір при наведенні (Primary Hover Hex)')
    )
    secondary_color = models.CharField(
        max_length=20,
        default='#059669',
        verbose_name=_('Додатковий колір (Secondary Hex)')
    )
    accent_color = models.CharField(
        max_length=20,
        default='#d97706',
        verbose_name=_('Акцентний колір (Accent Hex)')
    )
    font_family = models.CharField(
        max_length=100,
        default='Inter, system-ui, sans-serif',
        verbose_name=_('Основний шрифт')
    )

    class Meta:
        verbose_name = _('Налаштування теми та брендингу')
        verbose_name_plural = _('Налаштування тем та брендингу')

    def __str__(self):
        return f"Тема для {self.school.name}"
