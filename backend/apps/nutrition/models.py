from django.db import models
from django.utils.translation import gettext_lazy as _

class CateringProvider(models.Model):
    company_name = models.CharField(max_length=255, verbose_name=_('Організація, що надає послуги харчування'))
    edrpou = models.CharField(max_length=10, blank=True, verbose_name=_('Код ЄДРПОУ постачальника'))
    contract_number = models.CharField(max_length=100, verbose_name=_('Номер та дата договору'))
    contact_person = models.CharField(max_length=150, verbose_name=_('Відповідальна особа / технолог'))
    phone = models.CharField(max_length=50, verbose_name=_('Телефон для скарг та пропозицій'))

    class Meta:
        verbose_name = _('Організація харчування')
        verbose_name_plural = _('Організація харчування')

    def __str__(self):
        return self.company_name


class DailyMenu(models.Model):
    AGE_GROUPS = [
        ('1_4', _('1-4 класи (початкова школа)')),
        ('5_9', _('5-9 класи (базова школа)')),
        ('10_11', _('10-11 класи (старша школа)')),
    ]

    menu_date = models.DateField(verbose_name=_('Дата меню'))
    age_group = models.CharField(max_length=20, choices=AGE_GROUPS, default='1_4', verbose_name=_('Вікова група'))
    breakfast = models.TextField(blank=True, verbose_name=_('Сніданок (страви, вихід у грамах)'))
    lunch = models.TextField(blank=True, verbose_name=_('Обід (страви, вихід у грамах)'))
    snack = models.TextField(blank=True, verbose_name=_('Полуденок / підвечірок'))
    photo = models.ImageField(upload_to='nutrition/menus/%Y/%m/', blank=True, null=True, verbose_name=_('Фото меню з печаткою'))

    class Meta:
        verbose_name = _('Щоденне меню')
        verbose_name_plural = _('Щоденні меню харчування')
        ordering = ['-menu_date', 'age_group']
        unique_together = ('menu_date', 'age_group')

    def __str__(self):
        return f"Меню на {self.menu_date} ({self.get_age_group_display()})"
