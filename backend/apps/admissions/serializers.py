from rest_framework import serializers
from .models import ServiceTerritory, ClassCapacity, EnrolledStudent, AdmissionLottery

class ServiceTerritorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTerritory
        fields = ['id', 'street_name', 'building_numbers', 'district', 'decision_doc']

class EnrolledStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrolledStudent
        fields = ['id', 'last_name', 'enrollment_date', 'order_number', 'is_lottery']

class ClassCapacitySerializer(serializers.ModelSerializer):
    available_slots = serializers.IntegerField(read_only=True)
    students = EnrolledStudentSerializer(many=True, read_only=True)

    class Meta:
        model = ClassCapacity
        fields = ['id', 'grade_name', 'total_capacity', 'enrolled_count', 'available_slots', 'updated_at', 'students']

class AdmissionLotterySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionLottery
        fields = [
            'id', 'title', 'target_grade', 'lottery_datetime', 'location',
            'available_places', 'candidates_count', 'committee_order_doc', 'is_completed'
        ]
