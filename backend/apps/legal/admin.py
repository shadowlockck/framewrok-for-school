from django.contrib import admin
from .models import LegalDocumentCategory, LegalDocument, FinancialReport, StaffMember, Vacancy

@admin.register(LegalDocumentCategory)
class LegalDocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    ordering = ('order',)

@admin.register(LegalDocument)
class LegalDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'law_reference', 'approval_date', 'publish_date', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description', 'law_reference')

@admin.register(FinancialReport)
class FinancialReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'period', 'total_amount', 'approval_date', 'publish_date', 'is_within_10_days')
    list_filter = ('report_type', 'period')
    search_fields = ('title', 'notes')

@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'is_administration', 'category', 'pedagogical_title', 'last_qualification_update')
    list_filter = ('is_administration', 'category')
    search_fields = ('full_name', 'position')

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('position_title', 'is_director_vacancy', 'application_deadline', 'is_open')
    list_filter = ('is_director_vacancy', 'is_open')
    search_fields = ('position_title', 'requirements')
