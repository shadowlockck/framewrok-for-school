from rest_framework import serializers
from .models import CateringProvider, DailyMenu

class CateringProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CateringProvider
        fields = ['id', 'company_name', 'edrpou', 'contract_number', 'contact_person', 'phone']

class DailyMenuSerializer(serializers.ModelSerializer):
    age_group_display = serializers.CharField(source='get_age_group_display', read_only=True)

    class Meta:
        model = DailyMenu
        fields = [
            'id', 'menu_date', 'age_group', 'age_group_display',
            'breakfast', 'lunch', 'snack', 'photo'
        ]
