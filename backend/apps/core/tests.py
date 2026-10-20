from pathlib import Path
from django.test import RequestFactory, SimpleTestCase, TestCase, override_settings
from django.http import HttpResponse
from django.middleware.security import SecurityMiddleware
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

    def test_core_openapi_responses(self):
        response = self.client.get('/api/schema/?format=json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        schema = response.json()

        for path, component in (
            ('/api/v1/core/manifest/', 'SchoolManifest'),
            ('/api/v1/core/capabilities/', 'SchoolManifest'),
            ('/api/v1/core/compliance/', 'ComplianceReport'),
        ):
            with self.subTest(path=path):
                result = schema['paths'][path]['get']['responses']['200']
                self.assertEqual(
                    result['content']['application/json']['schema']['$ref'],
                    f'#/components/schemas/{component}',
                )

        components = schema['components']['schemas']
        self.assertEqual(
            set(components['SchoolManifest']['properties']),
            {'school', 'modules', 'navigation', 'compliance'},
        )
        self.assertEqual(
            set(components['ComplianceReport']['properties']),
            {
                'score', 'total_count', 'passed_count', 'warning_count',
                'danger_count', 'warnings', 'checks', 'is_fully_compliant',
            },
        )
        self.assertNotIn('id', components['ManifestSchool']['required'])
        self.assertNotIn('updated_at', components['ManifestSchool']['required'])
        self.assertNotIn('theme', components['ManifestSchool']['required'])
        self.assertTrue(components['ManifestSchool']['properties']['theme']['nullable'])

    def test_manifest_without_school_profile(self):
        self.profile.delete()
        response = self.client.get('/api/v1/core/manifest/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['school']['edrpou'], '')
        self.assertNotIn('id', response.json()['school'])

    def test_manifest_without_theme(self):
        self.theme.delete()
        response = self.client.get('/api/v1/core/manifest/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.json()['school']['theme'])

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


class SecuritySettingsTests(SimpleTestCase):
    @override_settings(
        SECURE_SSL_REDIRECT=True,
        SECURE_HSTS_SECONDS=300,
        SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https'),
        ALLOWED_HOSTS=['school.example'],
    )
    def test_https_redirect_and_hsts_with_trusted_proxy(self):
        middleware = SecurityMiddleware(lambda request: HttpResponse('ok'))
        factory = RequestFactory()
        plain_request = factory.get('/', HTTP_HOST='school.example')
        redirect = middleware(plain_request)
        self.assertEqual(redirect.status_code, 301)
        self.assertEqual(redirect['Location'], 'https://school.example/')

        proxied_request = factory.get(
            '/', HTTP_HOST='school.example', HTTP_X_FORWARDED_PROTO='https',
        )
        secure_response = middleware(proxied_request)
        self.assertEqual(secure_response.status_code, 200)
        self.assertEqual(secure_response['Strict-Transport-Security'], 'max-age=300')

    def test_source_and_generated_projects_support_direct_and_proxied_https(self):
        import json
        import os
        import subprocess
        import sys
        import tempfile
        from argparse import Namespace
        from .cli import cmd_startproject

        names = (
            'DEBUG', 'ALLOWED_HOSTS', 'SECURE_SSL_REDIRECT',
            'SECURE_PROXY_SSL_HEADER', 'SESSION_COOKIE_SECURE',
            'CSRF_COOKIE_SECURE', 'SECURE_HSTS_SECONDS',
            'SECURE_HSTS_INCLUDE_SUBDOMAINS', 'SECURE_HSTS_PRELOAD',
        )
        command = [
            sys.executable, '-c',
            'import json, runpy, sys; values = runpy.run_path(sys.argv[1]); '
            'print(json.dumps({name: values[name] for name in sys.argv[2:]}))',
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            cmd_startproject(Namespace(name='secure_school', output_dir=temp_dir))
            settings_files = (
                (Path(__file__).resolve().parents[2] / 'config' / 'settings.py', 'SECRET_KEY'),
                (Path(temp_dir) / 'secure_school' / 'config' / 'settings.py', 'DJANGO_SECRET_KEY'),
            )
            for settings_file, secret_name in settings_files:
                with self.subTest(settings_file=settings_file):
                    env = os.environ.copy()
                    env.update({
                        'DEBUG': 'False',
                        'ALLOWED_HOSTS': 'school.example',
                        'SECURE_HSTS_SECONDS': '300',
                        'TRUST_X_FORWARDED_PROTO': 'False',
                        secret_name: 'test-only-random-looking-secret-2457d15fc5c64d5282e754a769',
                    })
                    env.pop('SECURE_SSL_REDIRECT', None)
                    result = subprocess.run(
                        [*command, str(settings_file), *names], env=env,
                        capture_output=True, text=True, check=True,
                    )
                    settings = json.loads(result.stdout)
                    self.assertEqual(settings['ALLOWED_HOSTS'], ['school.example'])
                    self.assertTrue(settings['SECURE_SSL_REDIRECT'])
                    self.assertTrue(settings['SESSION_COOKIE_SECURE'])
                    self.assertTrue(settings['CSRF_COOKIE_SECURE'])
                    self.assertEqual(settings['SECURE_HSTS_SECONDS'], 300)
                    self.assertIsNone(settings['SECURE_PROXY_SSL_HEADER'])
                    self.assertFalse(settings['SECURE_HSTS_INCLUDE_SUBDOMAINS'])
                    self.assertFalse(settings['SECURE_HSTS_PRELOAD'])

                    env['TRUST_X_FORWARDED_PROTO'] = 'True'
                    proxied = subprocess.run(
                        [*command, str(settings_file), *names], env=env,
                        capture_output=True, text=True, check=True,
                    )
                    self.assertEqual(
                        json.loads(proxied.stdout)['SECURE_PROXY_SSL_HEADER'],
                        ['HTTP_X_FORWARDED_PROTO', 'https'],
                    )

                    env['ALLOWED_HOSTS'] = ''
                    missing_hosts = subprocess.run(
                        [*command, str(settings_file), *names], env=env,
                        capture_output=True, text=True,
                    )
                    self.assertNotEqual(missing_hosts.returncode, 0)
                    self.assertIn('Set ALLOWED_HOSTS', missing_hosts.stderr)

                    env['ALLOWED_HOSTS'] = 'school.example'
                    env.pop(secret_name)
                    missing_secret = subprocess.run(
                        [*command, str(settings_file), *names], env=env,
                        capture_output=True, text=True,
                    )
                    self.assertNotEqual(missing_secret.returncode, 0)
                    self.assertIn(secret_name, missing_secret.stderr)


class FrontendTemplateTests(SimpleTestCase):
    def test_three_templates_share_the_school_api_and_keep_classic_as_default(self):
        from argparse import Namespace
        import tempfile
        from .cli import cmd_create_frontend, cmd_startproject
        from .frontend_templates import FRONTEND_TEMPLATES

        with tempfile.TemporaryDirectory() as temp_dir:
            for template in FRONTEND_TEMPLATES:
                with self.subTest(template=template):
                    target = Path(temp_dir) / template
                    cmd_create_frontend(Namespace(
                        output_dir=target, api_url=None, force=False, template=template,
                    ))
                    app = (target / 'src' / 'App.tsx').read_text(encoding='utf-8')
                    css = (target / 'src' / 'index.css').read_text(encoding='utf-8')
                    package = (target / 'package.json').read_text(encoding='utf-8')
                    self.assertIn(f'school-site--{template}', app)
                    self.assertIn('/api/v1/core/manifest/', app)
                    self.assertIn('aria-current=', app)
                    self.assertIn('function Navigation(', app)
                    self.assertIn('function Safety(', app)
                    self.assertIn('function Gallery(', app)
                    self.assertIn(f'.school-site--{template}', css)
                    self.assertIn(FRONTEND_TEMPLATES[template]['label'], app)
                    self.assertIn('skip-link', app)
                    self.assertNotIn('tailwindcss', package)
                    self.assertNotIn('@tailwind', css)
                    self.assertFalse((target / 'postcss.config.js').exists())

            legacy_frontend = Path(temp_dir) / 'classic'
            (legacy_frontend / 'postcss.config.js').write_text(
                'export default {\n  plugins: {\n    tailwindcss: {},\n    autoprefixer: {},\n  },\n};\n',
                encoding='utf-8',
            )
            cmd_create_frontend(Namespace(
                output_dir=legacy_frontend, api_url=None, force=True, template='classic',
            ))
            self.assertFalse((legacy_frontend / 'postcss.config.js').exists())

            default = Path(temp_dir) / 'default'
            cmd_create_frontend(Namespace(output_dir=default, api_url=None, force=False))
            self.assertIn(
                'school-site--classic',
                (default / 'src' / 'App.tsx').read_text(encoding='utf-8'),
            )

            cmd_startproject(Namespace(
                name='site_with_frontend', output_dir=temp_dir,
                frontend_template='portal',
            ))
            generated = Path(temp_dir) / 'site_with_frontend' / 'frontend'
            self.assertIn(
                'school-site--portal',
                (generated / 'src' / 'App.tsx').read_text(encoding='utf-8'),
            )



