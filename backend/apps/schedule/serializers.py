from rest_framework import serializers
from .models import BellSchedule, LessonSchedule

class BellScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BellSchedule
        fields = ['id', 'lesson_number', 'start_time', 'end_time', 'break_duration']

class LessonScheduleSerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)
    grade_name = serializers.CharField(source='grade.grade_name', read_only=True)

    class Meta:
        model = LessonSchedule
        fields = ['id', 'grade', 'grade_name', 'day_of_week', 'day_name', 'lesson_number', 'subject', 'classroom', 'teacher_name']
