from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServiceTerritoryViewSet, ClassCapacityViewSet,
    EnrolledStudentViewSet, AdmissionLotteryViewSet
)

router = DefaultRouter()
router.register(r'territory', ServiceTerritoryViewSet, basename='admissions-territory')
router.register(r'capacity', ClassCapacityViewSet, basename='admissions-capacity')
router.register(r'students', EnrolledStudentViewSet, basename='admissions-students')
router.register(r'lottery', AdmissionLotteryViewSet, basename='admissions-lottery')

urlpatterns = [
    path('', include(router.urls)),
]
