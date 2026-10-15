from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolProfileViewSet, ThemeSettingsViewSet

router = DefaultRouter()
router.register(r'profile', SchoolProfileViewSet, basename='school-profile')
router.register(r'theme', ThemeSettingsViewSet, basename='school-theme')

urlpatterns = [
    path('', include(router.urls)),
]
