from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CateringProviderViewSet, DailyMenuViewSet

router = DefaultRouter()
router.register(r'provider', CateringProviderViewSet, basename='nutrition-provider')
router.register(r'menu', DailyMenuViewSet, basename='nutrition-menu')

urlpatterns = [
    path('', include(router.urls)),
]
