from rest_framework import serializers
from .models import PhotoAlbum, GalleryPhoto

class GalleryPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryPhoto
        fields = ['id', 'image', 'caption', 'order']

class PhotoAlbumSerializer(serializers.ModelSerializer):
    photos = GalleryPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = PhotoAlbum
        fields = ['id', 'title', 'description', 'cover_image', 'event_date', 'photos']
