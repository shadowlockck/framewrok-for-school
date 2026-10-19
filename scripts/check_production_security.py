"""Fail on Django deployment warnings except optional HSTS subdomain/preload policy."""

import os
from pathlib import Path
import sys


sys.path.insert(0, str(Path.cwd()))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django  # noqa: E402
from django.core.checks import run_checks  # noqa: E402
from django.core.checks.messages import WARNING  # noqa: E402


def main():
    django.setup()
    advisories = {"security.W005", "security.W021"}
    issues = run_checks(include_deployment_checks=True)
    failures = [issue for issue in issues if issue.level >= WARNING and issue.id not in advisories]
    if failures:
        for issue in failures:
            print(f"{issue.id}: {issue.msg}", file=sys.stderr)
        raise SystemExit(1)
    print("Deployment checks passed (HSTS subdomain/preload remain opt-in)")


if __name__ == "__main__":
    main()
