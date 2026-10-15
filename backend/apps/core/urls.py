from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolProfileViewSet, ThemeSettingsViewSet, SchoolManifestView

router = DefaultRouter()
router.register(r'profile', SchoolProfileViewSet, basename='school-profile')
router.register(r'theme', ThemeSettingsViewSet, basename='school-theme')

urlpatterns = [
    path('manifest/', SchoolManifestView.as_view(), name='school-manifest'),
    path('capabilities/', SchoolManifestView.as_view(), name='school-capabilities'),
    path('', include(router.urls)),
]
