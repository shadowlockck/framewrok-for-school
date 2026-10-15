from django.contrib import admin
from .models import PhotoAlbum, GalleryPhoto

class GalleryPhotoInline(admin.TabularInline):
    model = GalleryPhoto
    extra = 3
    fields = ('image', 'caption', 'order')

@admin.register(PhotoAlbum)
class PhotoAlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'created_at')
    search_fields = ('title', 'description')
    inlines = [GalleryPhotoInline]

@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('album', 'caption', 'order')
    list_filter = ('album',)
