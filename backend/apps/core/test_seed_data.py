from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.test import TestCase, override_settings

from apps.admissions.models import ClassCapacity
from apps.gallery.models import GalleryPhoto, PhotoAlbum
from apps.news.models import NewsArticle
from apps.nutrition.models import DailyMenu


class SeedSchoolDataTests(TestCase):
    def test_seed_populates_visible_sections_and_is_repeatable(self):
        with TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            call_command('seed_school_data', verbosity=0)

            self.assertGreaterEqual(NewsArticle.objects.filter(is_published=True).count(), 9)
            self.assertGreaterEqual(ClassCapacity.objects.count(), 8)
            self.assertEqual(DailyMenu.objects.count(), 6)
            self.assertEqual(PhotoAlbum.objects.count(), 4)
            self.assertEqual(GalleryPhoto.objects.count(), 5)
            for photo in GalleryPhoto.objects.all():
                self.assertTrue(photo.image.storage.exists(photo.image.name))

            article = NewsArticle.objects.get(title='Тиждень цифрової безпеки для учнів 5–9 класів')
            article.summary = 'Текст редактора'
            article.save(update_fields=['summary'])
            counts = (
                NewsArticle.objects.count(), ClassCapacity.objects.count(),
                DailyMenu.objects.count(), PhotoAlbum.objects.count(),
                GalleryPhoto.objects.count(),
            )

            call_command('seed_school_data', verbosity=0)

            self.assertEqual(counts, (
                NewsArticle.objects.count(), ClassCapacity.objects.count(),
                DailyMenu.objects.count(), PhotoAlbum.objects.count(),
                GalleryPhoto.objects.count(),
            ))
            article.refresh_from_db()
            self.assertEqual(article.summary, 'Текст редактора')
