from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PhotoAlbumViewSet, GalleryPhotoViewSet

router = DefaultRouter()
router.register(r'albums', PhotoAlbumViewSet, basename='gallery-albums')
router.register(r'photos', GalleryPhotoViewSet, basename='gallery-photos')

urlpatterns = [
    path('', include(router.urls)),
]
