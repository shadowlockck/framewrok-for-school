from pathlib import Path
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

    def test_compliance_auditor_and_api(self):
        from .compliance import ComplianceAuditor
        report = ComplianceAuditor.get_audit_report()
        self.assertIn('score', report)
        self.assertIn('checks', report)
        self.assertIn('warnings', report)
        self.assertTrue(report['total_count'] > 0)

        # Test API endpoint
        res = self.client.get('/api/v1/core/compliance/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertEqual(data['score'], report['score'])
        self.assertEqual(data['total_count'], report['total_count'])

    def test_admin_index_renders_compliance_dashboard(self):
        from django.contrib.auth.models import User
        admin_user = User.objects.create_superuser(username='admin_test', password='password123', email='admin@test.com')
        self.client.force_login(admin_user)
        res = self.client.get('/admin/')
        self.assertEqual(res.status_code, 200)
        content = res.content.decode('utf-8')
        self.assertIn('Монітор виконання ст. 30 ЗУ «Про освіту»', content)
        self.assertIn('Рівень відповідності', content)

    def test_public_home_renders(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.profile.name)

    def test_generated_project_requires_secret_in_production(self):
        from argparse import Namespace
        import os
        import subprocess
        import sys
        import tempfile
        from .cli import cmd_startproject

        with tempfile.TemporaryDirectory() as temp_dir:
            cmd_startproject(Namespace(name='production_check', output_dir=temp_dir))
            settings_path = Path(temp_dir) / 'production_check' / 'config' / 'settings.py'
            env = os.environ.copy()
            env['DEBUG'] = 'False'
            env.pop('DJANGO_SECRET_KEY', None)
            command = [sys.executable, '-c',
                       'import runpy, sys; config = runpy.run_path(sys.argv[1]); '
                       'print(config["CORS_ALLOW_ALL_ORIGINS"], config["ALLOWED_HOSTS"])',
                       str(settings_path)]

            missing_secret = subprocess.run(command, env=env, capture_output=True, text=True)
            self.assertNotEqual(missing_secret.returncode, 0)
            self.assertIn('Set DJANGO_SECRET_KEY', missing_secret.stderr)

            env['DJANGO_SECRET_KEY'] = 'a-test-secret-for-generated-project-settings'
            env['ALLOWED_HOSTS'] = 'school.example'
            configured = subprocess.run(command, env=env, capture_output=True, text=True)
            self.assertEqual(configured.returncode, 0, configured.stderr)
            self.assertIn("False ['school.example']", configured.stdout)

    def test_cli_startproject_and_school_creation(self):
        import tempfile
        import shutil
        from argparse import Namespace
        from .cli import cmd_startproject, cmd_create_school

        temp_dir = tempfile.mkdtemp()
        try:
            # Test startproject
            args_start = Namespace(name='test_school_cli', output_dir=temp_dir)
            cmd_startproject(args_start)
            project_path = Path(temp_dir) / 'test_school_cli'
            self.assertTrue((project_path / 'manage.py').exists())
            self.assertTrue((project_path / 'config' / 'settings.py').exists())

            # Test create-school
            args_create = Namespace(
                name='Нова Гімназія №12',
                short_name='Гімназія №12',
                edrpou='99887766',
                founder='Міська Рада',
                city='Львів',
                address='вул. Франка, 10',
                phone='+380 32 200-00-00',
                email='gymn12@lviv.ua',
                capacity=800,
                actual=750,
                language='Українська',
                primary_color='#2563eb'
            )
            cmd_create_school(args_create)
            school = SchoolProfile.objects.get(edrpou='99887766')
            self.assertEqual(school.name, 'Нова Гімназія №12')
            self.assertEqual(school.licensed_capacity, 800)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)



