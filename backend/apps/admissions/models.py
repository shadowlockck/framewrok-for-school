from django.db import models
from django.utils.translation import gettext_lazy as _

class ServiceTerritory(models.Model):
    street_name = models.CharField(max_length=200, verbose_name=_('Вулиця / проспект / провулок'))
    building_numbers = models.CharField(max_length=255, verbose_name=_('Номери будинків (діапазон або перелік)'))
    district = models.CharField(max_length=100, blank=True, verbose_name=_('Район міста / громада'))
    decision_doc = models.CharField(max_length=255, blank=True, verbose_name=_('Рішення / розпорядження про закріплення'))

    class Meta:
        verbose_name = _('Адреса закріпленої території')
        verbose_name_plural = _('Територія обслуговування (закріплені вулиці)')
        ordering = ['street_name']

    def __str__(self):
        return f"{self.street_name} ({self.building_numbers})"


class ClassCapacity(models.Model):
    grade_name = models.CharField(max_length=50, verbose_name=_('Клас / паралель (наприклад: 1-А, 10-А)'))
    total_capacity = models.PositiveIntegerField(verbose_name=_('Спроможність класу'))
    enrolled_count = models.PositiveIntegerField(verbose_name=_('Фактично зараховано'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата оновлення даних'))

    class Meta:
        verbose_name = _('Спроможність та вільні місця')
        verbose_name_plural = _('Наявність вільних місць у класах (п. 7 Порядку)')
        ordering = ['grade_name']

    def __str__(self):
        return f"{self.grade_name}: вільних {self.available_slots}"

    @property
    def available_slots(self):
        return max(0, self.total_capacity - self.enrolled_count)


class EnrolledStudent(models.Model):
    """
    ВАЖЛИВО: Дотримання Закону України «Про захист персональних даних».
    Оприлюднюються виключно прізвища зарахованих дітей!
    """
    last_name = models.CharField(max_length=100, verbose_name=_('Прізвище зарахованої дитини (виключно прізвище)'))
    grade = models.ForeignKey(ClassCapacity, on_delete=models.CASCADE, related_name='students', verbose_name=_('Клас'))
    enrollment_date = models.DateField(verbose_name=_('Дата зарахування'))
    order_number = models.CharField(max_length=100, blank=True, verbose_name=_('Номер наказу про зарахування'))
    is_lottery = models.BooleanField(default=False, verbose_name=_('Зараховано за результатами жеребкування'))

    class Meta:
        verbose_name = _('Зарахований учень (захист персональних даних)')
        verbose_name_plural = _('Списки зарахованих учнів (прізвища)')
        ordering = ['grade', 'last_name']

    def __str__(self):
        return f"{self.last_name} ({self.grade.grade_name})"


class AdmissionLottery(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Тема оголошення жеребкування'))
    target_grade = models.CharField(max_length=50, verbose_name=_('Клас для жеребкування'))
    lottery_datetime = models.DateTimeField(verbose_name=_('Дата і час проведення жеребкування'))
    location = models.CharField(max_length=255, verbose_name=_('Місце та спосіб проведення (актова зала, онлайн-трансляція)'))
    available_places = models.PositiveIntegerField(verbose_name=_('Кількість вільних місць'))
    candidates_count = models.PositiveIntegerField(verbose_name=_('Кількість дітей-претендентів'))
    committee_order_doc = models.FileField(
        upload_to='admissions/lottery/',
        verbose_name=_('Наказ про утворення конкурсної комісії з 3 осіб')
    )
    is_completed = models.BooleanField(default=False, verbose_name=_('Жеребкування проведено'))

    class Meta:
        verbose_name = _('Жеребкування на вільні місця')
        verbose_name_plural = _('Жеребкування на вільні місця')
        ordering = ['-lottery_datetime']

    def __str__(self):
        return f"{self.title} ({self.target_grade})"
