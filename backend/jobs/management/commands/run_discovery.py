from django.core.management.base import BaseCommand
from agent_engine.orchestrator import JobAgentOrchestrator

class Command(BaseCommand):
    help = 'Executes scheduled job discovery agent pipeline across active sources.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting South India Fresher Job Discovery pipeline...'))
        orchestrator = JobAgentOrchestrator()
        run = orchestrator.run_discovery()
        self.stdout.write(self.style.SUCCESS(
            f"Discovery completed with status: {run.status}\n"
            f"Jobs Discovered: {run.jobs_discovered}\n"
            f"Jobs Updated: {run.jobs_updated}\n"
            f"Ineligible Excluded: {run.ineligible_excluded}\n"
            f"Official Verified Count: {run.official_verified_count}"
        ))
