from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BellScheduleViewSet, LessonScheduleViewSet

router = DefaultRouter()
router.register(r'bells', BellScheduleViewSet, basename='schedule-bells')
router.register(r'lessons', LessonScheduleViewSet, basename='schedule-lessons')

urlpatterns = [
    path('', include(router.urls)),
]
