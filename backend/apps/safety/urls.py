from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AntiBullyingPolicyViewSet, ConfidentialReportViewSet

router = DefaultRouter()
router.register(r'policy', AntiBullyingPolicyViewSet, basename='safety-policy')
router.register(r'reports', ConfidentialReportViewSet, basename='safety-reports')

urlpatterns = [
    path('', include(router.urls)),
]
