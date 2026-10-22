"""Exercise the published installation path, outside the source checkout."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import sysconfig
import tempfile
from zipfile import ZipFile


REPO_ROOT = Path(__file__).resolve().parent.parent


def run(command, *, cwd, env=None):
    print(f"+ {' '.join(map(str, command))}", flush=True)
    subprocess.run([str(part) for part in command], cwd=cwd, env=env, check=True)


def probe_project(project):
    """Runs inside the fresh virtual environment after the site is migrated."""
    sys.path.insert(0, str(project))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    import apps.core
    import django
    from django.apps import apps as django_apps
    from django.contrib import admin as django_admin
    from django.contrib.auth import get_user_model
    from django.test import Client

    package_path = Path(apps.core.__file__).resolve()
    if not package_path.is_relative_to(Path(sys.prefix).resolve()):
        raise AssertionError(f"apps.core loaded outside installed environment: {package_path}")

    django.setup()
    from django.contrib.auth.models import Group
    client = Client()
    enabled = {name: django_apps.is_installed(f'apps.{name}') for name in (
        'legal', 'admissions', 'nutrition', 'safety', 'news', 'schedule', 'gallery'
    )}

    home = client.get("/")
    assert home.status_code == 200, f"Home returned {home.status_code}"
    assert "Тестова школа №1" in home.content.decode("utf-8")
    for name in ('legal', 'admissions', 'nutrition', 'safety'):
        if not enabled[name]:
            assert f'/api/v1/{name}/' not in home.content.decode('utf-8')

    manifest = client.get("/api/v1/core/manifest/")
    assert manifest.status_code == 200
    assert manifest.json()["school"]["name"] == "Тестова школа №1"
    assert manifest.json()["modules"] == enabled
    assert manifest.json()['compliance']['article_30'] == enabled['legal']
    assert {item['id'] for item in manifest.json()['navigation']}.issubset(
        {name for name, active in enabled.items() if active} | ({'finance'} if enabled['legal'] else set())
    )
    for name in enabled:
        response = client.get(f'/api/v1/{name}/')
        assert response.status_code == (200 if enabled[name] else 404), (name, response.status_code)

    registered_apps = {model._meta.app_label for model in django_admin.site._registry}
    for name in enabled:
        if not enabled[name]:
            assert name not in registered_apps, name

    schema = client.get('/api/schema/?format=json').json()['paths']
    for name in enabled:
        assert any(path.startswith(f'/api/v1/{name}/') for path in schema) == enabled[name], name

    if enabled['safety']:
        from apps.safety.models import ConfidentialReport
        report = client.post(
            "/api/v1/safety/reports/",
            data=json.dumps({
                "reporter_role": "witness",
                "incident_description": "Тестове звернення зі встановленого пакета",
            }, ensure_ascii=False),
            content_type="application/json",
        )
        assert report.status_code == 201, f"Report returned {report.status_code}: {report.content!r}"
        assert ConfidentialReport.objects.filter(reporter_role="witness").count() == 1
        assert client.get("/api/v1/safety/reports/").status_code == 405

    admin = get_user_model().objects.create_superuser(
        "smoke_admin", "smoke@example.test", "test-password"
    )
    client.force_login(admin)
    dashboard = client.get("/admin/")
    assert dashboard.status_code == 200
    assert "Монітор виконання ст. 30" in dashboard.content.decode("utf-8")
    from apps.core.roles import group_name, role_specs
    editor_group = Group.objects.get(name=group_name(role_specs()['content_admin']))
    assert not editor_group.permissions.filter(content_type__app_label='auth').exists()
    assert not editor_group.permissions.filter(content_type__model='confidentialreport').exists()
    if enabled['news']:
        editor = get_user_model().objects.create_user('smoke_editor', password='test-password', is_staff=True)
        editor.groups.add(Group.objects.get(name=group_name(role_specs()['news_editor'])))
        client.force_login(editor)
        assert client.get('/admin/news/newsarticle/add/').status_code == 200
        assert client.get('/admin/core/schoolprofile/').status_code == 403
        if enabled['safety']:
            assert client.get('/admin/safety/confidentialreport/').status_code == 403
    print(f"Installed package: {package_path}", flush=True)
    print("Backend smoke checks passed", flush=True)


OPTIONAL_MODULES = ('legal', 'admissions', 'nutrition', 'safety', 'news', 'schedule', 'gallery')


def probe_optional_projects(*, workdir, python, school_admin, env):
    """Exercise independent settings in fresh processes against the installed wheel."""
    subsets = [('core_only', ())]
    if os.name != 'nt':
        subsets += [(f'only_{name}', (name,)) for name in OPTIONAL_MODULES if name != 'schedule']
        subsets += [(f'without_{name}', tuple(mod for mod in OPTIONAL_MODULES if mod != name))
                    for name in OPTIONAL_MODULES if name != 'admissions']
        subsets += [('without_admissions_schedule', tuple(
            mod for mod in OPTIONAL_MODULES if mod not in ('admissions', 'schedule')
        ))]
    subsets += [('with_schedule', ('admissions', 'schedule'))]

    for project_name, selected in subsets:
        run([school_admin, 'startproject', project_name, '--output-dir', workdir], cwd=workdir, env=env)
        project = workdir / project_name
        settings_file = project / 'config' / 'settings.py'
        settings_text = settings_file.read_text(encoding='utf-8')
        for name in OPTIONAL_MODULES:
            if name not in selected:
                settings_text = settings_text.replace(f"    'apps.{name}',\n", '')
        settings_file.write_text(settings_text, encoding='utf-8')
        run([python, 'manage.py', 'check'], cwd=project, env=env)
        run([python, 'manage.py', 'migrate', '--noinput'], cwd=project, env=env)
        run([python, 'manage.py', 'setup_school_roles'], cwd=project, env=env)
        run([python, 'manage.py', 'setup_school_roles'], cwd=project, env=env)
        run([python, 'manage.py', 'makemigrations', '--check', '--dry-run'], cwd=project, env=env)
        run([python, 'manage.py', 'seed_school_data'], cwd=project, env=env)
        run([school_admin, 'create-school', 'Тестова школа №1', '--edrpou', '12345678'], cwd=project, env=env)
        run([python, '-I', __file__, '--probe-project', project], cwd=project, env=env)

    project = workdir / 'invalid_schedule'
    run([school_admin, 'startproject', project.name, '--output-dir', workdir], cwd=workdir, env=env)
    settings_file = project / 'config' / 'settings.py'
    settings_file.write_text(
        settings_file.read_text(encoding='utf-8').replace("    'apps.admissions',\n", ''),
        encoding='utf-8',
    )
    bad = subprocess.run([str(python), 'manage.py', 'check'], cwd=project, env=env,
                         capture_output=True, text=True)
    assert bad.returncode != 0 and 'school.E001' in bad.stderr, bad.stderr


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-frontend", action="store_true", help="Skip npm build on Python-only runners")
    parser.add_argument("--probe-project", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.probe_project is not None:
        probe_project(args.probe_project.resolve())
        return

    skip_frontend = args.skip_frontend or os.environ.get("SMOKE_SKIP_FRONTEND") == "1"

    with tempfile.TemporaryDirectory(prefix="school-package-smoke-") as temp_name:
        workdir = Path(temp_name).resolve()
        wheel_dir = workdir / "wheels"
        wheel_dir.mkdir()
        run([
            sys.executable, "-m", "pip", "wheel", "--no-deps", "--no-build-isolation",
            "--no-index", "--wheel-dir", wheel_dir, REPO_ROOT / "backend",
        ], cwd=workdir)
        wheels = list(wheel_dir.glob("django_school_framework-*.whl"))
        if len(wheels) != 1:
            raise AssertionError(f"Expected one framework wheel, found {wheels}")
        with ZipFile(wheels[0]) as artifact:
            files = set(artifact.namelist())
            required = {
                "apps/core/frontend_templates.py",
                "apps/core/modules.py",
                "apps/core/roles.py",
                "apps/core/management/commands/setup_school_roles.py",
                "apps/core/templates/school/home.html",
                "apps/core/templates/admin/index.html",
                "apps/core/templates/admin/compliance_dashboard.html",
                "apps/safety/migrations/0002_alter_confidentialreport_reporter_role.py",
            }
            if missing := required - files:
                raise AssertionError(f"Wheel is missing: {sorted(missing)}")

        virtualenv = workdir / "venv"
        offline = os.environ.get('SMOKE_USE_SYSTEM_SITE_PACKAGES') == '1'
        run([sys.executable, "-m", "venv", *(['--system-site-packages'] if offline else []), virtualenv], cwd=workdir)
        scripts_dir = virtualenv / ("Scripts" if os.name == "nt" else "bin")
        python = scripts_dir / ("python.exe" if os.name == "nt" else "python")
        school_admin = scripts_dir / ("school-admin.exe" if os.name == "nt" else "school-admin")
        if offline:
            site_packages = (virtualenv / 'Lib' / 'site-packages' if os.name == 'nt'
                             else virtualenv / 'lib' / f'python{sys.version_info.major}.{sys.version_info.minor}' / 'site-packages')
            (site_packages / 'local-dependencies.pth').write_text(
                sysconfig.get_paths()['purelib'] + '\n', encoding='utf-8'
            )
        run([python, "-m", "pip", "install", *(['--no-deps'] if offline else []), wheels[0]], cwd=workdir)

        env = os.environ.copy()
        for name in ("PYTHONPATH", "DJANGO_SETTINGS_MODULE", "DB_ENGINE", "DJANGO_SECRET_KEY"):
            env.pop(name, None)
        env.update(DEBUG="True", ALLOWED_HOSTS="testserver,localhost,127.0.0.1")
        run([
            school_admin, "startproject", "smoke_school", "--output-dir", workdir,
            "--frontend-template", "portal",
        ], cwd=workdir, env=env)
        project = workdir / "smoke_school"
        generated_app = (project / "frontend" / "src" / "App.tsx").read_text(encoding="utf-8")
        assert "school-site--portal" in generated_app
        run([python, "manage.py", "migrate", "--noinput"], cwd=project, env=env)
        run([python, "manage.py", "setup_school_roles"], cwd=project, env=env)
        run([python, "manage.py", "setup_school_roles", "--dry-run"], cwd=project, env=env)
        run([python, "manage.py", "makemigrations", "--check", "--dry-run"], cwd=project, env=env)
        run([python, "manage.py", "check"], cwd=project, env=env)
        run([
            python, "manage.py", "spectacular", "--validate", "--fail-on-warn",
            "--file", workdir / "openapi.yaml",
        ], cwd=project, env=env)
        prod_env = env.copy()
        prod_env.update(
            DEBUG="False",
            DJANGO_SECRET_KEY="smoke-deploy-check-key-29bd93b56aa34db9862b11119fe3a53e",
            ALLOWED_HOSTS="school.example",
            SECURE_HSTS_SECONDS="300",
        )
        run([python, "-I", REPO_ROOT / "scripts" / "check_production_security.py"], cwd=project, env=prod_env)
        run([school_admin, "create-school", "Тестова школа №1", "--edrpou", "12345678"], cwd=project, env=env)
        run([python, "-I", __file__, "--probe-project", project], cwd=project, env=env)
        run([python, 'manage.py', 'seed_school_data'], cwd=project, env=env)
        settings_file = project / 'config' / 'settings.py'
        original_settings = settings_file.read_text(encoding='utf-8')
        settings_file.write_text(original_settings.replace("    'apps.gallery',\n", ''), encoding='utf-8')
        run([python, 'manage.py', 'check'], cwd=project, env=env)
        run([python, 'manage.py', 'shell', '-c',
             "from django.test import Client; assert Client().get('/api/v1/gallery/albums/').status_code == 404"],
            cwd=project, env=env)
        settings_file.write_text(original_settings, encoding='utf-8')
        run([python, 'manage.py', 'shell', '-c',
             "from apps.gallery.models import PhotoAlbum; from django.test import Client; "
             "assert PhotoAlbum.objects.exists(); "
             "assert Client().get('/api/v1/gallery/albums/').status_code == 200"],
            cwd=project, env=env)
        probe_optional_projects(workdir=workdir, python=python, school_admin=school_admin, env=env)

        if not skip_frontend:
            frontend = workdir / "frontend"
            run([school_admin, "create-frontend", "--output-dir", frontend], cwd=workdir, env=env)
            npm = shutil.which("npm")
            if not npm:
                raise RuntimeError("npm is required to build the generated frontend")
            run([npm, "install", "--no-audit", "--no-fund"], cwd=frontend, env=env)
            run([npm, "run", "build"], cwd=frontend, env=env)
            print("Generated frontend build passed", flush=True)


if __name__ == "__main__":
    main()
