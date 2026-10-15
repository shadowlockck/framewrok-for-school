from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import SchoolProfile, ThemeSettings
from .serializers import SchoolProfileSerializer, ThemeSettingsSerializer

class SchoolProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SchoolProfile.objects.all()
    serializer_class = SchoolProfileSerializer
    permission_classes = [permissions.AllowAny]

class ThemeSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ThemeSettings.objects.all()
    serializer_class = ThemeSettingsSerializer
    permission_classes = [permissions.AllowAny]
