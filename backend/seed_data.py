#!/usr/bin/env python
"""
Seed script to initialize sources and populate live verified jobs.
"""
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    import django
    django.setup()

    from agent_engine.orchestrator import JobAgentOrchestrator
    from jobs.models import Job
    from job_sources.models import JobSource

    print("Populating sources and running autonomous discovery sweep...")
    orchestrator = JobAgentOrchestrator()
    run = orchestrator.run_discovery()

    print(f"\n[DONE] Discovery Run Status: {run.status}")
    print(f"Total Eligible Jobs in DB: {Job.objects.filter(eligibility_classification='ELIGIBLE_FRESHER').count()}")
    print(f"Total Ineligible Excluded: {Job.objects.filter(eligibility_classification='INELIGIBLE_EXPERIENCED').count()}")
    print(f"Total Sources Polled: {JobSource.objects.count()}")

if __name__ == '__main__':
    main()
