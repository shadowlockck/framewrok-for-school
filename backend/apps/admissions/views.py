from rest_framework import viewsets, permissions, filters
from .models import ServiceTerritory, ClassCapacity, EnrolledStudent, AdmissionLottery
from .serializers import (
    ServiceTerritorySerializer, ClassCapacitySerializer,
    EnrolledStudentSerializer, AdmissionLotterySerializer
)

class ServiceTerritoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceTerritory.objects.all()
    serializer_class = ServiceTerritorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['street_name', 'building_numbers']

class ClassCapacityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClassCapacity.objects.all()
    serializer_class = ClassCapacitySerializer
    permission_classes = [permissions.AllowAny]

class EnrolledStudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EnrolledStudent.objects.all().select_related('grade')
    serializer_class = EnrolledStudentSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['last_name']

class AdmissionLotteryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AdmissionLottery.objects.all()
    serializer_class = AdmissionLotterySerializer
    permission_classes = [permissions.AllowAny]
