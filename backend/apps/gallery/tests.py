from datetime import date
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import PhotoAlbum, GalleryPhoto

class GalleryTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.album = PhotoAlbum.objects.create(
            title='Свято першого дзвоника',
            description='Урочиста лінійка 1 вересня',
            event_date=date(2026, 9, 1)
        )
        self.photo = GalleryPhoto.objects.create(
            album=self.album,
            caption='Першокласники з квітами',
            order=1
        )

    def test_str_representations(self):
        self.assertEqual(str(self.album), 'Свято першого дзвоника (2026-09-01)')
        self.assertEqual(str(self.photo), 'Фото в альбомі Свято першого дзвоника')

    def test_albums_api_list(self):
        res = self.client.get('/api/v1/gallery/albums/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        results = data.get('results', data)
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]['title'], 'Свято першого дзвоника')
