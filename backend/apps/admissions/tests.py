from django.test import TestCase
from datetime import date
from .models import ClassCapacity, EnrolledStudent

class AdmissionsComplianceTests(TestCase):
    def setUp(self):
        self.capacity = ClassCapacity.objects.create(
            grade_name='1-А',
            total_capacity=30,
            enrolled_count=28
        )

    def test_available_slots_calculation(self):
        self.assertEqual(self.capacity.available_slots, 2)

    def test_personal_data_protection(self):
        """
        Перевірка дотримання ЗУ «Про захист персональних даних»:
        У списках оприлюднюються виключно прізвища здобувачів освіти.
        """
        student = EnrolledStudent.objects.create(
            last_name='Коваленко',
            grade=self.capacity,
            enrollment_date=date(2026, 6, 1),
            order_number='№ 12-У'
        )
        self.assertEqual(student.last_name, 'Коваленко')
        self.assertFalse(hasattr(student, 'first_name'))
        self.assertFalse(hasattr(student, 'passport_or_birth_cert'))
