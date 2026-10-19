"""Exercise the published installation path, outside the source checkout."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
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
    from django.contrib.auth import get_user_model
    from django.test import Client

    package_path = Path(apps.core.__file__).resolve()
    if not package_path.is_relative_to(Path(sys.prefix).resolve()):
        raise AssertionError(f"apps.core loaded outside installed environment: {package_path}")

    django.setup()
    from apps.safety.models import ConfidentialReport
    client = Client()

    home = client.get("/")
    assert home.status_code == 200, f"Home returned {home.status_code}"
    assert "Тестова школа №1" in home.content.decode("utf-8")

    manifest = client.get("/api/v1/core/manifest/")
    assert manifest.status_code == 200
    assert manifest.json()["school"]["name"] == "Тестова школа №1"

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
    print(f"Installed package: {package_path}", flush=True)
    print("Backend smoke checks passed", flush=True)


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
                "apps/core/templates/school/home.html",
                "apps/core/templates/admin/index.html",
                "apps/core/templates/admin/compliance_dashboard.html",
                "apps/safety/migrations/0002_alter_confidentialreport_reporter_role.py",
            }
            if missing := required - files:
                raise AssertionError(f"Wheel is missing: {sorted(missing)}")

        virtualenv = workdir / "venv"
        run([sys.executable, "-m", "venv", virtualenv], cwd=workdir)
        scripts_dir = virtualenv / ("Scripts" if os.name == "nt" else "bin")
        python = scripts_dir / ("python.exe" if os.name == "nt" else "python")
        school_admin = scripts_dir / ("school-admin.exe" if os.name == "nt" else "school-admin")
        run([python, "-m", "pip", "install", wheels[0]], cwd=workdir)

        env = os.environ.copy()
        for name in ("PYTHONPATH", "DJANGO_SETTINGS_MODULE", "DB_ENGINE", "DJANGO_SECRET_KEY"):
            env.pop(name, None)
        env.update(DEBUG="True", ALLOWED_HOSTS="testserver,localhost,127.0.0.1")
        run([school_admin, "startproject", "smoke_school", "--output-dir", workdir], cwd=workdir, env=env)
        project = workdir / "smoke_school"
        run([python, "manage.py", "migrate", "--noinput"], cwd=project, env=env)
        run([python, "manage.py", "makemigrations", "--check", "--dry-run"], cwd=project, env=env)
        run([python, "manage.py", "check"], cwd=project, env=env)
        run([
            python, "manage.py", "spectacular", "--validate", "--fail-on-warn",
            "--file", workdir / "openapi.yaml",
        ], cwd=project, env=env)
        run([school_admin, "create-school", "Тестова школа №1", "--edrpou", "12345678"], cwd=project, env=env)
        run([python, "-I", __file__, "--probe-project", project], cwd=project, env=env)

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
