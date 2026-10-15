from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import SchoolProfile, ThemeSettings

class CoreModelAndApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.profile = SchoolProfile.objects.create(
            name='Ліцей №1 м. Києва',
            short_name='Ліцей №1',
            edrpou='12345678',
            founder='Київська міська рада',
            address='вул. Хрещатик, 1, м. Київ',
            phone='+380 44 111-22-33',
            email='school1@kyiv.edu.ua',
            licensed_capacity=1000,
            actual_students=950,
            education_language='Українська'
        )
        self.theme = ThemeSettings.objects.create(
            school=self.profile,
            primary_color='#1e3a8a',
            primary_hover='#172554',
            secondary_color='#059669',
            accent_color='#d97706'
        )

    def test_school_profile_str(self):
        self.assertEqual(str(self.profile), 'Ліцей №1 м. Києва (ЄДРПОУ 12345678)')

    def test_theme_settings_str(self):
        self.assertIn('Ліцей №1 м. Києва', str(self.theme))

    def test_profile_api_read_only(self):
        res = self.client.get('/api/v1/core/profile/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        results = data.get('results', data)
        self.assertTrue(len(results) > 0)
        item = results[0]
        self.assertEqual(item['edrpou'], '12345678')
        self.assertIn('theme', item)
        self.assertEqual(item['theme']['primary_color'], '#1e3a8a')

    def test_manifest_capabilities_api(self):
        res = self.client.get('/api/v1/core/manifest/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertIn('school', data)
        self.assertEqual(data['school']['name'], 'Ліцей №1 м. Києва')
        self.assertIn('modules', data)
        self.assertTrue(data['modules']['legal'])
        self.assertIn('navigation', data)
        self.assertTrue(len(data['navigation']) > 0)
        self.assertIn('compliance', data)
        self.assertTrue(data['compliance']['article_30'])

