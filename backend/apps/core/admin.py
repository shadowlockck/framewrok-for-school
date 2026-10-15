from django.contrib import admin
from .models import SchoolProfile, ThemeSettings

class ThemeSettingsInline(admin.StackedInline):
    model = ThemeSettings
    can_delete = False
    verbose_name = "Налаштування теми та кольорів сайту"

@admin.register(SchoolProfile)
class SchoolProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'edrpou', 'founder', 'licensed_capacity', 'actual_students', 'updated_at')
    search_fields = ('name', 'edrpou', 'founder')
    inlines = [ThemeSettingsInline]

@admin.register(ThemeSettings)
class ThemeSettingsAdmin(admin.ModelAdmin):
    list_display = ('school', 'primary_color', 'secondary_color', 'accent_color', 'font_family')
