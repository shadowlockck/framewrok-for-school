from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.admissions.models import ClassCapacity

class BellSchedule(models.Model):
    lesson_number = models.PositiveSmallIntegerField(unique=True, verbose_name=_('Номер уроку'))
    start_time = models.TimeField(verbose_name=_('Початок уроку'))
    end_time = models.TimeField(verbose_name=_('Кінець уроку'))
    break_duration = models.PositiveSmallIntegerField(default=10, verbose_name=_('Тривалість перерви (хв)'))

    class Meta:
        verbose_name = _('Розклад дзвінка')
        verbose_name_plural = _('Розклад дзвінків')
        ordering = ['lesson_number']

    def __str__(self):
        return f"{self.lesson_number} урок: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"


class LessonSchedule(models.Model):
    DAYS_OF_WEEK = [
        (1, _('Понеділок')),
        (2, _('Вівторок')),
        (3, _('Середа')),
        (4, _('Четвер')),
        (5, _('П’ятниця')),
    ]

    grade = models.ForeignKey(ClassCapacity, on_delete=models.CASCADE, related_name='lessons', verbose_name=_('Клас'))
    day_of_week = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK, verbose_name=_('День тижня'))
    lesson_number = models.PositiveSmallIntegerField(verbose_name=_('Номер уроку'))
    subject = models.CharField(max_length=150, verbose_name=_('Предмет / навчальний курс'))
    classroom = models.CharField(max_length=50, blank=True, verbose_name=_('Кабінет'))
    teacher_name = models.CharField(max_length=150, blank=True, verbose_name=_('Вчитель'))

    class Meta:
        verbose_name = _('Урок у розкладі')
        verbose_name_plural = _('Розклад уроків')
        ordering = ['grade', 'day_of_week', 'lesson_number']
        unique_together = ('grade', 'day_of_week', 'lesson_number')

    def __str__(self):
        return f"{self.grade.grade_name} | {self.get_day_of_week_display()} #{self.lesson_number} {self.subject}"
