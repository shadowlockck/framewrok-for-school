from django.contrib import admin
from .models import AntiBullyingPolicy, ConfidentialReport

@admin.register(AntiBullyingPolicy)
class AntiBullyingPolicyAdmin(admin.ModelAdmin):
    list_display = ('title', 'academic_year', 'is_active')
    list_filter = ('is_active', 'academic_year')

@admin.register(ConfidentialReport)
class ConfidentialReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'reporter_role', 'created_at', 'is_reviewed')
    list_filter = ('reporter_role', 'is_reviewed', 'created_at')
    readonly_fields = ('reporter_role', 'incident_description', 'contact_feedback', 'created_at')
    fieldsets = (
        ('Дані звернення (Конфіденційно)', {
            'fields': ('reporter_role', 'incident_description', 'contact_feedback', 'created_at')
        }),
        ('Опрацювання комісією закладу освіти', {
            'fields': ('is_reviewed', 'review_notes')
        }),
    )
