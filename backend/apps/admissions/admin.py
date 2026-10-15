from django.contrib import admin
from .models import ServiceTerritory, ClassCapacity, EnrolledStudent, AdmissionLottery

class EnrolledStudentInline(admin.TabularInline):
    model = EnrolledStudent
    extra = 1
    fields = ('last_name', 'enrollment_date', 'order_number', 'is_lottery')

@admin.register(ServiceTerritory)
class ServiceTerritoryAdmin(admin.ModelAdmin):
    list_display = ('street_name', 'building_numbers', 'district')
    search_fields = ('street_name', 'building_numbers')

@admin.register(ClassCapacity)
class ClassCapacityAdmin(admin.ModelAdmin):
    list_display = ('grade_name', 'total_capacity', 'enrolled_count', 'available_slots', 'updated_at')
    inlines = [EnrolledStudentInline]

@admin.register(EnrolledStudent)
class EnrolledStudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'grade', 'enrollment_date', 'order_number', 'is_lottery')
    list_filter = ('grade', 'is_lottery')
    search_fields = ('last_name',)

@admin.register(AdmissionLottery)
class AdmissionLotteryAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_grade', 'lottery_datetime', 'available_places', 'candidates_count', 'is_completed')
    list_filter = ('is_completed',)
