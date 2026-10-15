from datetime import time
from django.test import TestCase
from django.db import IntegrityError
from rest_framework.test import APIClient
from rest_framework import status
from apps.admissions.models import ClassCapacity
from .models import BellSchedule, LessonSchedule

class ScheduleTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.grade = ClassCapacity.objects.create(
            grade_name='5-А',
            total_capacity=30,
            enrolled_count=28
        )
        self.bell = BellSchedule.objects.create(
            lesson_number=1,
            start_time=time(8, 30),
            end_time=time(9, 15),
            break_duration=10
        )
        self.lesson = LessonSchedule.objects.create(
            grade=self.grade,
            day_of_week=1,
            lesson_number=1,
            subject='Українська мова',
            classroom='Кабінет 204',
            teacher_name='Осадча В.О.'
        )

    def test_str_representations(self):
        self.assertIn('1 урок', str(self.bell))
        self.assertIn('5-А', str(self.lesson))
        self.assertIn('Українська мова', str(self.lesson))

    def test_unique_lesson_slot(self):
        with self.assertRaises(IntegrityError):
            LessonSchedule.objects.create(
                grade=self.grade,
                day_of_week=1,
                lesson_number=1,
                subject='Математика'
            )

    def test_schedule_apis(self):
        res_bell = self.client.get('/api/v1/schedule/bells/')
        self.assertEqual(res_bell.status_code, status.HTTP_200_OK)

        res_lessons = self.client.get('/api/v1/schedule/lessons/')
        self.assertEqual(res_lessons.status_code, status.HTTP_200_OK)
