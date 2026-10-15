from rest_framework import viewsets, permissions, filters
from .models import LegalDocumentCategory, LegalDocument, FinancialReport, StaffMember, Vacancy
from .serializers import (
    LegalDocumentCategorySerializer, LegalDocumentSerializer,
    FinancialReportSerializer, StaffMemberSerializer, VacancySerializer
)

class LegalDocumentCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LegalDocumentCategory.objects.all()
    serializer_class = LegalDocumentCategorySerializer
    permission_classes = [permissions.AllowAny]

class LegalDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LegalDocument.objects.filter(is_active=True).select_related('category')
    serializer_class = LegalDocumentSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'law_reference']

class FinancialReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FinancialReport.objects.all()
    serializer_class = FinancialReportSerializer
    permission_classes = [permissions.AllowAny]

class StaffMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StaffMember.objects.all()
    serializer_class = StaffMemberSerializer
    permission_classes = [permissions.AllowAny]

class VacancyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vacancy.objects.filter(is_open=True)
    serializer_class = VacancySerializer
    permission_classes = [permissions.AllowAny]
