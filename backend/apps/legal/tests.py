from django.test import TestCase
from datetime import date, timedelta
from .models import LegalDocumentCategory, LegalDocument, FinancialReport

class LegalComplianceTests(TestCase):
    def setUp(self):
        self.category = LegalDocumentCategory.objects.create(name='Установчі документи', order=1)

    def test_legal_document_creation(self):
        doc = LegalDocument.objects.create(
            category=self.category,
            title='Статут ліцею',
            law_reference='ст. 30 ЗУ «Про освіту»',
            is_active=True
        )
        self.assertEqual(str(doc), 'Статут ліцею')
        self.assertTrue(doc.is_active)

    def test_financial_report_10_days_deadline(self):
        # Оприлюднено вчасно (7 днів)
        ontime_report = FinancialReport.objects.create(
            title='Кошторис 2026',
            report_type='estimate',
            period='2026',
            total_amount=100000.00,
            approval_date=date(2026, 9, 1),
            publish_date=date(2026, 9, 8),
            file='test.pdf'
        )
        self.assertTrue(ontime_report.is_within_10_days)

        # Оприлюднено із запізненням (понад 14 календарних днів)
        late_report = FinancialReport.objects.create(
            title='Звіт Q1',
            report_type='quarterly_report',
            period='Q1 2026',
            total_amount=50000.00,
            approval_date=date(2026, 1, 1),
            publish_date=date(2026, 2, 1),
            file='test2.pdf'
        )
        self.assertFalse(late_report.is_within_10_days)
