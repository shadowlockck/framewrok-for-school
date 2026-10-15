from rest_framework import viewsets, permissions, mixins
from .models import AntiBullyingPolicy, ConfidentialReport
from .serializers import AntiBullyingPolicySerializer, ConfidentialReportSerializer

class AntiBullyingPolicyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AntiBullyingPolicy.objects.filter(is_active=True)
    serializer_class = AntiBullyingPolicySerializer
    permission_classes = [permissions.AllowAny]

class ConfidentialReportViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Дозволяє будь-якому користувачеві (учень, батьки, вчитель) конфіденційно надіслати заяву.
    Перегляд доступний виключно в адмін-панелі уповноваженою комісією.
    """
    queryset = ConfidentialReport.objects.all()
    serializer_class = ConfidentialReportSerializer
    permission_classes = [permissions.AllowAny]
