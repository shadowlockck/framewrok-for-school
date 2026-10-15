from rest_framework import viewsets, permissions, filters
from .models import BellSchedule, LessonSchedule
from .serializers import BellScheduleSerializer, LessonScheduleSerializer

class BellScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BellSchedule.objects.all()
    serializer_class = BellScheduleSerializer
    permission_classes = [permissions.AllowAny]

class LessonScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LessonSchedule.objects.all().select_related('grade')
    serializer_class = LessonScheduleSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['grade__grade_name', 'subject', 'teacher_name']
