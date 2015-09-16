#!/usr/bin/env python
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


if not settings.configured:
    settings.configure(
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        INSTALLED_APPS = [
            'smartforms', 'tests',
        ]
    )


if __name__ == "__main__":
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    suite = [sys.argv[1]] if len(sys.argv) > 1 else ["tests"]
    failures = test_runner.run_tests(suite)
    sys.exit(bool(failures))
