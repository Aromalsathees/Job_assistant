import time
import logging
from django.utils import timezone
from typing import Dict, Any, List

from job_sources.models import JobSource
from job_sources.adapters import (
    ArbeitnowAdapter,
    RemotiveAdapter,
    TechnoparkAdapter,
    InfoparkAdapter,
    SouthIndiaDirectAdapter,
)
from discovery_runs.models import DiscoveryRun
from .normalization_service import NormalizationService
from .eligibility_service import EligibilityAgent
from .verification_service import VerificationService
from .deduplication_service import DuplicateDetectionService
from .ranking_service import RankingService
from .persistence_service import PersistenceService

logger = logging.getLogger(__name__)

ADAPTER_REGISTRY = {
    'technopark_kerala': TechnoparkAdapter,
    'infopark_kerala': InfoparkAdapter,
    'south_india_direct': SouthIndiaDirectAdapter,
    'remotive_api': RemotiveAdapter,
    'arbeitnow_api': ArbeitnowAdapter,
}

class JobAgentOrchestrator:
    """
    Coordinates the 9-stage Agentic Job Discovery Workflow.
    Ensures bounded retries, detailed audit run logs, and strict eligibility enforcement.
    """

    def __init__(self, target_roles: List[str] = None, target_locations: List[str] = None):
        self.target_roles = target_roles or ['Python', 'Django', 'FastAPI', 'Agentic AI', 'React']
        self.target_locations = target_locations or ['Kochi', 'Thiruvananthapuram', 'Chennai', 'Bengaluru']
        self.eligibility_agent = EligibilityAgent()
        self.verification_service = VerificationService()

    def run_discovery(self) -> DiscoveryRun:
        """
        Executes end-to-end discovery across all active registered sources.
        """
        start_time = time.time()
        now = timezone.now()

        # Create DiscoveryRun record in RUNNING state
        run_record = DiscoveryRun.objects.create(
            status='RUNNING',
            started_at=now,
        )

        sources_checked = []
        sources_failed = []
        discovered_count = 0
        updated_count = 0
        duplicates_skipped = 0
        ineligible_excluded = 0
        unclear_separated = 0
        official_verified_count = 0
        trusted_board_count = 0

        # Ensure seed sources exist in DB if not already populated
        self._ensure_default_sources()

        active_sources = JobSource.objects.filter(is_active=True)

        for source in active_sources:
            adapter_cls = ADAPTER_REGISTRY.get(source.code)
            if not adapter_cls:
                logger.warning(f"No adapter registered for source code: {source.code}")
                continue

            sources_checked.append(source.name)
            adapter = adapter_cls(config=source.config)

            try:
                raw_items = adapter.fetch_raw_jobs(limit=25)
                source_jobs_found = 0

                for raw_item in raw_items:
                    try:
                        # 1. Normalization
                        norm = NormalizationService.normalize(raw_item)
                        norm['source_code'] = source.code

                        # 2. Strict Eligibility Classification
                        eligibility = self.eligibility_agent.evaluate(norm)
                        norm.update(eligibility)

                        # Count metrics
                        if norm['eligibility_classification'] == 'INELIGIBLE_EXPERIENCED':
                            ineligible_excluded += 1
                        elif norm['eligibility_classification'] == 'ELIGIBILITY_UNCLEAR':
                            unclear_separated += 1

                        # 3. Authenticity & Verification
                        norm['source_type'] = source.source_type
                        verification = self.verification_service.verify(norm)
                        norm.update(verification)

                        if norm['verification_status'] == 'OFFICIAL_VERIFIED':
                            official_verified_count += 1
                        elif norm['verification_status'] == 'TRUSTED_BOARD':
                            trusted_board_count += 1

                        # 4. Duplicate Identification
                        job_uid = DuplicateDetectionService.generate_job_uid(norm)
                        norm['job_uid'] = job_uid

                        # 5. Ranking computation
                        norm['ranking_score'] = RankingService.calculate_score(norm)

                        # 6. Atomic Persistence
                        job_inst, is_created = PersistenceService.persist_job(
                            source=source,
                            job_data=norm,
                            job_uid=job_uid
                        )

                        if is_created:
                            discovered_count += 1
                        else:
                            updated_count += 1

                        source_jobs_found += 1

                    except Exception as item_err:
                        logger.error(f"Error processing item from {source.name}: {item_err}")

                source.last_polled_at = timezone.now()
                source.total_jobs_found += source_jobs_found
                source.save()

            except Exception as src_err:
                logger.error(f"Failed discovery on source {source.name}: {src_err}")
                sources_failed.append(f"{source.name}: {str(src_err)}")

        duration = round(time.time() - start_time, 2)
        final_status = 'SUCCESS' if not sources_failed else ('PARTIAL_SUCCESS' if discovered_count > 0 else 'FAILED')

        # Update run record
        run_record.status = final_status
        run_record.completed_at = timezone.now()
        run_record.duration_seconds = duration
        run_record.sources_checked = sources_checked
        run_record.sources_failed = sources_failed
        run_record.jobs_discovered = discovered_count
        run_record.jobs_updated = updated_count
        run_record.duplicates_skipped = duplicates_skipped
        run_record.ineligible_excluded = ineligible_excluded
        run_record.unclear_separated = unclear_separated
        run_record.official_verified_count = official_verified_count
        run_record.trusted_board_count = trusted_board_count
        run_record.summary_notes = (
            f"Discovery completed in {duration}s. {discovered_count} new jobs added, "
            f"{updated_count} existing jobs updated, {ineligible_excluded} ineligible roles strictly excluded, "
            f"{unclear_separated} classified as experience unclear."
        )
        run_record.save()

        return run_record

    def _ensure_default_sources(self):
        """Initializes default sources in DB if table is empty."""
        defaults = [
            {
                'name': 'Technopark Careers Portal',
                'code': 'technopark_kerala',
                'source_type': 'OFFICIAL_PORTAL',
                'base_url': 'https://www.technopark.in/job-search',
                'trust_rating': 5,
            },
            {
                'name': 'Infopark Kochi Official Portal',
                'code': 'infopark_kerala',
                'source_type': 'OFFICIAL_PORTAL',
                'base_url': 'https://infopark.in/companies/job-search',
                'trust_rating': 5,
            },
            {
                'name': 'South India Direct Employer Feeds',
                'code': 'south_india_direct',
                'source_type': 'DIRECT_EMPLOYER',
                'base_url': 'https://keralait.org',
                'trust_rating': 5,
            },
            {
                'name': 'Remotive Remote API',
                'code': 'remotive_api',
                'source_type': 'PUBLIC_API',
                'base_url': 'https://remotive.com/api/remote-jobs',
                'trust_rating': 4,
            },
            {
                'name': 'Arbeitnow Public API',
                'code': 'arbeitnow_api',
                'source_type': 'PUBLIC_API',
                'base_url': 'https://www.arbeitnow.com/api/job-board-api',
                'trust_rating': 4,
            },
        ]
        for d in defaults:
            JobSource.objects.get_or_create(code=d['code'], defaults=d)
