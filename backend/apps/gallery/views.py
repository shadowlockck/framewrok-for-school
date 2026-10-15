from rest_framework import viewsets, permissions, filters
from .models import PhotoAlbum, GalleryPhoto
from .serializers import PhotoAlbumSerializer, GalleryPhotoSerializer

class PhotoAlbumViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PhotoAlbum.objects.all()
    serializer_class = PhotoAlbumSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

class GalleryPhotoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GalleryPhoto.objects.all()
    serializer_class = GalleryPhotoSerializer
    permission_classes = [permissions.AllowAny]
