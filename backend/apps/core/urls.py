from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolProfileViewSet, ThemeSettingsViewSet, SchoolManifestView, ComplianceAuditView

router = DefaultRouter()
router.register(r'profile', SchoolProfileViewSet, basename='school-profile')
router.register(r'theme', ThemeSettingsViewSet, basename='school-theme')

urlpatterns = [
    path('manifest/', SchoolManifestView.as_view(), name='school-manifest'),
    path('capabilities/', SchoolManifestView.as_view(), name='school-capabilities'),
    path('compliance/', ComplianceAuditView.as_view(), name='school-compliance'),
    path('', include(router.urls)),
]
