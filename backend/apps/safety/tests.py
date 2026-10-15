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
        report = ConfidentialReport.objects.first()
        self.assertFalse(report.is_reviewed)
