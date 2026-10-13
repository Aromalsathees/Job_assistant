#!/usr/bin/env python
import os
import sys

def run_all_tests():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    import django
    django.setup()
    from django.test.runner import DiscoverRunner

    runner = DiscoverRunner(verbosity=2, interactive=False)
    failures = runner.run_tests([
        'jobs',
        'agent_engine.tests',
        'applications',
    ])
    if failures:
        print(f"\n[FAIL] {failures} test suite failure(s) detected.")
        sys.exit(1)
    else:
        print("\n[SUCCESS] All test suites passed successfully!")
        sys.exit(0)

if __name__ == '__main__':
    run_all_tests()
