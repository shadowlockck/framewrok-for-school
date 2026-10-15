from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LegalDocumentCategoryViewSet, LegalDocumentViewSet,
    FinancialReportViewSet, StaffMemberViewSet, VacancyViewSet
)

router = DefaultRouter()
router.register(r'categories', LegalDocumentCategoryViewSet, basename='legal-categories')
router.register(r'documents', LegalDocumentViewSet, basename='legal-documents')
router.register(r'finance', FinancialReportViewSet, basename='legal-finance')
router.register(r'staff', StaffMemberViewSet, basename='legal-staff')
router.register(r'vacancies', VacancyViewSet, basename='legal-vacancies')

urlpatterns = [
    path('', include(router.urls)),
]
