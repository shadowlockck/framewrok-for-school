from rest_framework import serializers
from .models import SchoolProfile, ThemeSettings

class ThemeSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemeSettings
        fields = ['primary_color', 'primary_hover', 'secondary_color', 'accent_color', 'font_family']

class SchoolProfileSerializer(serializers.ModelSerializer):
    theme = ThemeSettingsSerializer(read_only=True)

    class Meta:
        model = SchoolProfile
        fields = [
            'id', 'name', 'short_name', 'edrpou', 'founder', 'address',
            'phone', 'email', 'website', 'licensed_capacity', 'actual_students',
            'education_language', 'logo', 'theme', 'updated_at'
        ]
