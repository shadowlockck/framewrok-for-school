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


class ManifestSchoolSerializer(SchoolProfileSerializer):
    # The manifest also works before the first SchoolProfile is created.
    id = serializers.IntegerField(required=False)
    updated_at = serializers.DateTimeField(required=False)
    theme = ThemeSettingsSerializer(required=False, allow_null=True)


class ManifestModulesSerializer(serializers.Serializer):
    legal = serializers.BooleanField()
    admissions = serializers.BooleanField()
    nutrition = serializers.BooleanField()
    safety = serializers.BooleanField()
    news = serializers.BooleanField()
    schedule = serializers.BooleanField()
    gallery = serializers.BooleanField()


class ManifestNavigationSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    icon = serializers.CharField()


class ManifestComplianceSerializer(serializers.Serializer):
    article_30 = serializers.BooleanField()
    wcag_version = serializers.CharField()
    privacy_law_enforced = serializers.BooleanField()
    financial_deadline_days = serializers.IntegerField()


class SchoolManifestSerializer(serializers.Serializer):
    school = ManifestSchoolSerializer()
    modules = ManifestModulesSerializer()
    navigation = ManifestNavigationSerializer(many=True)
    compliance = ManifestComplianceSerializer()


class ComplianceCheckSerializer(serializers.Serializer):
    code = serializers.CharField()
    title = serializers.CharField()
    law_ref = serializers.CharField()
    status = serializers.ChoiceField(choices=['ok', 'warning', 'danger'])
    message = serializers.CharField()
    admin_url = serializers.CharField()


class ComplianceReportSerializer(serializers.Serializer):
    score = serializers.IntegerField()
    total_count = serializers.IntegerField()
    passed_count = serializers.IntegerField()
    warning_count = serializers.IntegerField()
    danger_count = serializers.IntegerField()
    warnings = serializers.ListField(child=serializers.CharField())
    checks = ComplianceCheckSerializer(many=True)
    is_fully_compliant = serializers.BooleanField()
