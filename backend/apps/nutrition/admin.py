from django.contrib import admin
from .models import CateringProvider, DailyMenu

@admin.register(CateringProvider)
class CateringProviderAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'edrpou', 'contract_number', 'contact_person', 'phone')

@admin.register(DailyMenu)
class DailyMenuAdmin(admin.ModelAdmin):
    list_display = ('menu_date', 'age_group')
    list_filter = ('age_group', 'menu_date')
    date_hierarchy = 'menu_date'
