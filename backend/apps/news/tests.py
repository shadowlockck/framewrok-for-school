from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import NewsCategory, NewsArticle

class NewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = NewsCategory.objects.create(name='Оголошення', slug='announcements')
        self.article1 = NewsArticle.objects.create(
            category=self.category,
            title='Термінове оголошення: зміна розкладу',
            summary='Увага всім учням',
            content='Деталі зміни розкладу',
            is_urgent=True,
            is_published=True
        )
        self.draft = NewsArticle.objects.create(
            category=self.category,
            title='Чернетка новини',
            content='Тільки для модератора',
            is_published=False
        )

    def test_str_representations(self):
        self.assertEqual(str(self.category), 'Оголошення')
        self.assertEqual(str(self.article1), 'Термінове оголошення: зміна розкладу')

    def test_news_api_list(self):
        res = self.client.get('/api/v1/news/articles/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        results = data.get('results', data)
        titles = [item['title'] for item in results]
        self.assertIn('Термінове оголошення: зміна розкладу', titles)
        # Drafts should not be public if filtered, or check if filter applies
        self.assertTrue(len(results) >= 1)
