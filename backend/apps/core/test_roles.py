"""End-to-end checks for editor roles and Django Admin authorization."""

from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command, CommandError
from django.test import Client, TestCase
from django.urls import reverse

from apps.admissions.models import ClassCapacity, EnrolledStudent
from apps.news.models import NewsArticle
from apps.safety.models import ConfidentialReport
from apps.schedule.models import LessonSchedule
from apps.core.roles import GROUP_PREFIX, group_name, role_specs


class EditorRolesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('setup_school_roles', stdout=StringIO())

    def staff(self, name, *roles):
        user = get_user_model().objects.create_user(username=name, password='test-password', is_staff=True)
        user.groups.add(*(Group.objects.get(name=group_name(role_specs()[key])) for key in roles))
        self.client.force_login(user)
        return user

    def test_sync_is_exact_idempotent_and_dry_run_is_read_only(self):
        news = Group.objects.get(name=group_name(role_specs()['news_editor']))
        extra = Permission.objects.get(content_type__app_label='auth', codename='change_user')
        news.permissions.add(extra)
        count = Group.objects.filter(name__startswith=GROUP_PREFIX).count()
        output = StringIO()
        call_command('setup_school_roles', '--dry-run', stdout=output)
        self.assertIn('прибрати 1', output.getvalue())
        self.assertIn('- auth.change_user', output.getvalue())
        self.assertTrue(news.permissions.filter(pk=extra.pk).exists())
        call_command('setup_school_roles', stdout=StringIO())
        self.assertFalse(news.permissions.filter(pk=extra.pk).exists())
        call_command('setup_school_roles', stdout=output)
        self.assertEqual(Group.objects.filter(name__startswith=GROUP_PREFIX).count(), count)
        self.assertIn('0 груп оновлено', output.getvalue())
        content = Group.objects.get(name=group_name(role_specs()['content_admin']))
        self.assertFalse(content.permissions.filter(content_type__app_label='auth').exists())
        self.assertFalse(content.permissions.filter(content_type__model='confidentialreport').exists())

    def test_disabled_group_loses_rights_without_losing_members(self):
        user = self.staff('editor', 'news_editor')
        news = Group.objects.get(name=group_name(role_specs()['news_editor']))
        enabled = {module: module != 'news' for module in (
            'legal', 'admissions', 'nutrition', 'safety', 'news', 'schedule', 'gallery'
        )}
        with patch('apps.core.roles.installed_modules', return_value=enabled):
            call_command('setup_school_roles', stdout=StringIO())
        self.assertEqual(news.permissions.count(), 0)
        self.assertTrue(user.groups.filter(pk=news.pk).exists())
        call_command('setup_school_roles', stdout=StringIO())
        self.assertTrue(news.permissions.exists())

    def test_missing_permission_fails_before_changing_groups(self):
        group = Group.objects.get(name=group_name(role_specs()['news_editor']))
        before = set(group.permissions.values_list('pk', flat=True))
        Permission.objects.get(content_type__app_label='legal', codename='view_financialreport').delete()
        with self.assertRaisesMessage(CommandError, 'Спочатку виконайте manage.py migrate'):
            call_command('setup_school_roles', stdout=StringIO())
        self.assertEqual(set(group.permissions.values_list('pk', flat=True)), before)

    def test_multiple_groups_and_revocation(self):
        user = self.staff('two_roles', 'news_editor', 'gallery_editor')
        news_url = reverse('admin:news_newsarticle_changelist')
        gallery_url = reverse('admin:gallery_photoalbum_changelist')
        self.assertEqual(self.client.get(news_url).status_code, 200)
        self.assertEqual(self.client.get(gallery_url).status_code, 200)
        user.groups.remove(Group.objects.get(name=group_name(role_specs()['news_editor'])))
        self.assertEqual(self.client.get(news_url).status_code, 403)
        self.assertEqual(self.client.get(gallery_url).status_code, 200)

    def test_news_editor_publishes_and_cannot_open_other_sections(self):
        self.staff('news', 'news_editor')
        add = reverse('admin:news_newsarticle_add')
        self.assertEqual(self.client.get(add).status_code, 200)
        response = self.client.post(add, {
            'title': 'Шкільна новина', 'content': 'Оголошення', 'summary': '',
            'is_published': 'on',
        })
        self.assertEqual(response.status_code, 302)
        article = NewsArticle.objects.get(title='Шкільна новина')
        self.assertEqual(self.client.get('/api/v1/news/articles/').json()['count'], 1)
        change = reverse('admin:news_newsarticle_change', args=[article.pk])
        response = self.client.post(change, {
            'title': article.title, 'content': article.content, 'summary': '',
        })
        self.assertEqual(response.status_code, 302)
        article.refresh_from_db()
        self.assertFalse(article.is_published)
        self.assertEqual(self.client.get('/api/v1/news/articles/').json()['count'], 0)
        self.assertEqual(self.client.get(reverse('admin:legal_financialreport_changelist')).status_code, 403)
        self.assertEqual(self.client.post(reverse('admin:legal_financialreport_add'), {}).status_code, 403)
        self.assertEqual(self.client.get(reverse('admin:safety_confidentialreport_changelist')).status_code, 403)
        self.assertEqual(self.client.post('/api/v1/news/articles/', {'title': 'Обхід'}).status_code, 405)

    def test_content_admin_and_safety_editor_cannot_read_reports(self):
        for role in ('content_admin', 'safety_editor'):
            with self.subTest(role=role):
                self.client.logout()
                self.staff(role, role)
                self.assertEqual(self.client.get(reverse('admin:safety_confidentialreport_changelist')).status_code, 403)
                self.assertEqual(self.client.get(reverse('admin:auth_user_changelist')).status_code, 403)
        self.assertEqual(self.client.get(reverse('admin:safety_antibullyingpolicy_changelist')).status_code, 200)

    def test_reviewer_can_process_but_not_alter_submitted_report(self):
        report = ConfidentialReport.objects.create(reporter_role='student', incident_description='Початковий опис')
        self.staff('reviewer', 'reports_reviewer')
        url = reverse('admin:safety_confidentialreport_change', args=[report.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        response = self.client.post(url, {
            'reporter_role': 'teacher', 'incident_description': 'Підміна',
            'contact_feedback': 'stolen@example.test', 'is_reviewed': 'on',
            'review_notes': 'Опрацьовано',
        })
        self.assertEqual(response.status_code, 302)
        report.refresh_from_db()
        self.assertEqual(report.reporter_role, 'student')
        self.assertEqual(report.incident_description, 'Початковий опис')
        self.assertEqual(report.contact_feedback, '')
        self.assertTrue(report.is_reviewed)
        self.assertEqual(report.review_notes, 'Опрацьовано')
        self.assertEqual(self.client.get(reverse('admin:safety_confidentialreport_add')).status_code, 403)
        self.assertEqual(self.client.post(reverse('admin:safety_confidentialreport_delete', args=[report.pk])).status_code, 403)
        self.assertEqual(self.client.get('/api/v1/safety/reports/').status_code, 405)

    def test_schedule_editor_can_view_class_but_not_students(self):
        self.staff('schedule', 'schedule_editor')
        cls = ClassCapacity.objects.create(grade_name='1-А', total_capacity=30, enrolled_count=0)
        EnrolledStudent.objects.create(grade=cls, last_name='Тестова', enrollment_date='2026-09-01')
        add = reverse('admin:schedule_lessonschedule_add')
        self.assertEqual(self.client.get(add).status_code, 200)
        self.assertEqual(self.client.post(add, {
            'grade': cls.pk, 'day_of_week': 1, 'lesson_number': 1, 'subject': 'Українська мова',
            'classroom': '12', 'teacher_name': 'Учитель',
        }).status_code, 302)
        self.assertTrue(LessonSchedule.objects.filter(grade=cls, subject='Українська мова').exists())
        self.assertEqual(self.client.get(reverse('admin:admissions_classcapacity_changelist')).status_code, 200)
        detail = self.client.get(reverse('admin:admissions_classcapacity_change', args=[cls.pk]))
        self.assertEqual(detail.status_code, 200)
        self.assertNotContains(detail, 'Тестова')
        self.assertEqual(self.client.post(reverse('admin:admissions_classcapacity_change', args=[cls.pk]), {
            'grade_name': 'Підміна', 'total_capacity': 0, 'enrolled_count': 0,
        }).status_code, 403)
        self.assertEqual(self.client.get(reverse('admin:admissions_enrolledstudent_changelist')).status_code, 403)
        cls.refresh_from_db()
        self.assertEqual(cls.grade_name, '1-А')

    def test_admissions_editor_cannot_cascade_delete_unauthorized_lesson(self):
        self.staff('admissions', 'admissions_editor')
        cls = ClassCapacity.objects.create(grade_name='2-Б', total_capacity=30, enrolled_count=0)
        lesson = LessonSchedule.objects.create(grade=cls, day_of_week=1, lesson_number=1, subject='Математика')
        url = reverse('admin:admissions_classcapacity_delete', args=[cls.pk])
        self.assertEqual(self.client.post(url, {'post': 'yes'}).status_code, 403)
        self.assertTrue(ClassCapacity.objects.filter(pk=cls.pk).exists())
        self.assertTrue(LessonSchedule.objects.filter(pk=lesson.pk).exists())

    def test_admissions_editor_cannot_bulk_delete_class_with_lessons(self):
        self.staff('admissions_bulk', 'admissions_editor')
        cls = ClassCapacity.objects.create(grade_name='3-В', total_capacity=30, enrolled_count=0)
        lesson = LessonSchedule.objects.create(grade=cls, day_of_week=1, lesson_number=1, subject='Математика')
        response = self.client.post(reverse('admin:admissions_classcapacity_changelist'), {
            'action': 'delete_selected', '_selected_action': [cls.pk], 'post': 'yes',
        })
        self.assertEqual(response.status_code, 403)
        self.assertTrue(ClassCapacity.objects.filter(pk=cls.pk).exists())
        self.assertTrue(LessonSchedule.objects.filter(pk=lesson.pk).exists())

    def test_admin_post_requires_csrf_token(self):
        user = self.staff('csrf', 'news_editor')
        client = Client(enforce_csrf_checks=True)
        client.force_login(user)
        response = client.post(reverse('admin:news_newsarticle_add'), {
            'title': 'Без токена', 'content': 'Текст', 'is_published': 'on',
        })
        self.assertEqual(response.status_code, 403)
        self.assertFalse(NewsArticle.objects.filter(title='Без токена').exists())

    def test_audit_links_follow_permissions_without_changing_score(self):
        self.staff('editor', 'news_editor')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '/admin/legal/legaldocument/')
        self.assertNotContains(response, '/admin/core/schoolprofile/')
        public_score = self.client.get('/api/v1/core/compliance/').json()['score']
        self.assertIn(f'{public_score}%', response.content.decode())

    def test_staff_without_permissions_and_superuser(self):
        self.staff('empty')
        self.assertEqual(self.client.get(reverse('admin:news_newsarticle_changelist')).status_code, 403)
        self.client.logout()
        admin = get_user_model().objects.create_superuser(username='super', password='test-password')
        self.client.force_login(admin)
        self.assertEqual(self.client.get(reverse('admin:safety_confidentialreport_changelist')).status_code, 200)
