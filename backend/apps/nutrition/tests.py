from datetime import date
from django.test import TestCase
from django.db import IntegrityError
from rest_framework.test import APIClient
from rest_framework import status
from .models import CateringProvider, DailyMenu

class NutritionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.provider = CateringProvider.objects.create(
            company_name='ТОВ "Якісне харчування"',
            edrpou='87654321',
            contract_number='№ 12-2026',
            contact_person='Шевченко Ірина',
            phone='+380 44 999-88-77'
        )
        self.menu = DailyMenu.objects.create(
            menu_date=date.today(),
            age_group='1_4',
            breakfast='Каша з молоком',
            lunch='Суп та пюре з рибою'
        )

    def test_provider_str(self):
        self.assertEqual(str(self.provider), 'ТОВ "Якісне харчування"')

    def test_daily_menu_unique_per_day_and_age_group(self):
        with self.assertRaises(IntegrityError):
            DailyMenu.objects.create(
                menu_date=date.today(),
                age_group='1_4',
                breakfast='Дубльоване меню'
            )

    def test_nutrition_apis(self):
        res_provider = self.client.get('/api/v1/nutrition/providers/')
        self.assertEqual(res_provider.status_code, status.HTTP_200_OK)

        res_menu = self.client.get('/api/v1/nutrition/daily-menus/')
        self.assertEqual(res_menu.status_code, status.HTTP_200_OK)
