from django.test import TestCase
from rest_framework.test import APIClient
from .models import ConfidentialReport

class SafetyTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_confidential_report_submission(self):
        """Перевірка можливості анонімного надсилання заяви про булінг через API"""
        payload = {
            'reporter_role': 'anonymous',
            'incident_description': 'Тестове повідомлення про факт цькування в коридорі.',
            'contact_feedback': 'test@example.com'
        }
        response = self.client.post('/api/v1/safety/reports/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ConfidentialReport.objects.count(), 1)
    def test_confidential_report_by_witness(self):
        """Перевірка ролі 'свідок події' при надсиланні заяви"""
        payload = {
            'reporter_role': 'witness',
            'incident_description': 'Помічено булінг на шкільному подвір\'ї.',
        }
        response = self.client.post('/api/v1/safety/reports/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        report = ConfidentialReport.objects.get(reporter_role='witness')
        self.assertEqual(report.reporter_role, 'witness')

    def test_confidential_report_with_logged_in_session(self):
        """Перевірка, що користувач із активною сесією (наприклад адмін) може відправити форму без CSRF помилки"""
        from django.contrib.auth.models import User
        user = User.objects.create_user(username='staff', password='pwd')
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(user)
        payload = {
            'reporter_role': 'student',
            'incident_description': 'Звернення від учня під час сесії.',
        }
        response = client.post('/api/v1/safety/reports/', payload, format='json')
        self.assertEqual(response.status_code, 201)
