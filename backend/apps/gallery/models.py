from django.db import models
from django.utils.translation import gettext_lazy as _

class PhotoAlbum(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Назва альбому / події'))
    description = models.TextField(blank=True, verbose_name=_('Опис події'))
    cover_image = models.ImageField(upload_to='gallery/covers/%Y/', blank=True, null=True, verbose_name=_('Обкладинка альбому'))
    event_date = models.DateField(verbose_name=_('Дата заходу'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Фотоальбом')
        verbose_name_plural = _('Фотоальбоми')
        ordering = ['-event_date']

    def __str__(self):
        return f"{self.title} ({self.event_date})"


class GalleryPhoto(models.Model):
    album = models.ForeignKey(PhotoAlbum, on_delete=models.CASCADE, related_name='photos', verbose_name=_('Альбом'))
    image = models.ImageField(upload_to='gallery/photos/%Y/%m/', verbose_name=_('Фотографія'))
    caption = models.CharField(max_length=255, blank=True, verbose_name=_('Підпис до фото'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('Порядок відображення'))

    class Meta:
        verbose_name = _('Фотографія галереї')
        verbose_name_plural = _('Фотографії галереї')
        ordering = ['order', 'id']

    def __str__(self):
        return f"Фото в альбомі {self.album.title}"
