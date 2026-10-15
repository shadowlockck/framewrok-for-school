from rest_framework import serializers
from .models import LegalDocumentCategory, LegalDocument, FinancialReport, StaffMember, Vacancy

class LegalDocumentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalDocumentCategory
        fields = ['id', 'name', 'order']

class LegalDocumentSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = LegalDocument
        fields = [
            'id', 'category', 'category_name', 'title', 'law_reference',
            'description', 'file', 'external_url', 'approval_date', 'publish_date', 'is_active'
        ]

class FinancialReportSerializer(serializers.ModelSerializer):
    is_within_10_days = serializers.BooleanField(read_only=True)

    class Meta:
        model = FinancialReport
        fields = [
            'id', 'title', 'report_type', 'period', 'total_amount',
            'approval_date', 'publish_date', 'file', 'notes', 'is_within_10_days'
        ]

class StaffMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffMember
        fields = [
            'id', 'full_name', 'position', 'is_administration', 'category',
            'pedagogical_title', 'education', 'last_qualification_update', 'photo'
        ]

class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = [
            'id', 'position_title', 'salary_conditions', 'requirements',
            'is_director_vacancy', 'application_deadline', 'contact_person', 'is_open'
        ]
