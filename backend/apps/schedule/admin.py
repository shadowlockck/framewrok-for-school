from django.contrib import admin
from .models import BellSchedule, LessonSchedule

@admin.register(BellSchedule)
class BellScheduleAdmin(admin.ModelAdmin):
    list_display = ('lesson_number', 'start_time', 'end_time', 'break_duration')

@admin.register(LessonSchedule)
class LessonScheduleAdmin(admin.ModelAdmin):
    list_display = ('grade', 'day_of_week', 'lesson_number', 'subject', 'classroom', 'teacher_name')
    list_filter = ('grade', 'day_of_week')
    search_fields = ('subject', 'teacher_name', 'classroom')
