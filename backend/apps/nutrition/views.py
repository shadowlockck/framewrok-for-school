from rest_framework import viewsets, permissions
from .models import CateringProvider, DailyMenu
from .serializers import CateringProviderSerializer, DailyMenuSerializer

class CateringProviderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CateringProvider.objects.all()
    serializer_class = CateringProviderSerializer
    permission_classes = [permissions.AllowAny]

class DailyMenuViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DailyMenu.objects.all()
    serializer_class = DailyMenuSerializer
    permission_classes = [permissions.AllowAny]
