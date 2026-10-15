from rest_framework import serializers
from .models import AntiBullyingPolicy, ConfidentialReport

class AntiBullyingPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = AntiBullyingPolicy
        fields = [
            'id', 'title', 'academic_year', 'behavior_rules_doc',
            'application_procedure_doc', 'reaction_procedure_doc',
            'action_plan_doc', 'is_active'
        ]

class ConfidentialReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfidentialReport
        fields = ['id', 'reporter_role', 'incident_description', 'contact_feedback', 'created_at']
        read_only_fields = ['id', 'created_at']
