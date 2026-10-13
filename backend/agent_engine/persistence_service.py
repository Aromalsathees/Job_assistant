import logging
from django.db import transaction
from django.utils import timezone
from typing import Dict, Any, Tuple
from jobs.models import Job, VerificationRecord, ProvenanceSnapshot
from job_sources.models import JobSource

logger = logging.getLogger(__name__)

class PersistenceService:
    """
    Handles atomic persistence of validated job items into the relational schema.
    Guarantees idempotency and maintains verification records and raw provenance.
    """

    @classmethod
    def persist_job(cls, source: JobSource, job_data: Dict[str, Any], job_uid: str) -> Tuple[Job, bool]:
        """
        Idempotently inserts or updates a job.
        Returns (job_instance, is_created).
        """
        with transaction.atomic():
            # Check existing job
            existing = Job.objects.filter(job_uid=job_uid).first()
            
            job_fields = {
                'title': job_data['title'],
                'company_name': job_data['company_name'],
                'location': job_data['location'],
                'city': job_data['city'],
                'state': job_data['state'],
                'work_mode': job_data['work_mode'],
                'employment_type': job_data['employment_type'],
                'experience_min_months': job_data['experience_min_months'],
                'experience_max_months': job_data['experience_max_months'],
                'experience_raw_text': job_data['experience_raw_text'],
                'eligibility_category': job_data['eligibility_category'],
                'eligibility_classification': job_data['eligibility_classification'],
                'eligibility_reason': job_data['eligibility_reason'],
                'required_skills': job_data['required_skills'],
                'preferred_skills': job_data['preferred_skills'],
                'salary_disclosed': job_data['salary_disclosed'],
                'salary_min': job_data['salary_min'],
                'salary_max': job_data['salary_max'],
                'salary_currency': job_data['salary_currency'],
                'salary_raw_text': job_data['salary_raw_text'],
                'original_description': job_data['original_description'],
                'ai_summary': job_data['ai_summary'],
                'original_url': job_data['original_url'],
                'official_apply_url': job_data['official_apply_url'],
                'verification_status': job_data['verification_status'],
                'verification_notes': job_data.get('verification_notes', ''),
                'ranking_score': job_data['ranking_score'],
                'is_available': job_data.get('is_available', True),
                'source': source,
                'source_job_id': job_data['source_job_id'],
            }

            if existing:
                # Update existing record
                for k, v in job_fields.items():
                    setattr(existing, k, v)
                existing.last_checked_at = timezone.now()
                existing.save()
                job = existing
                is_created = False
            else:
                job = Job.objects.create(job_uid=job_uid, **job_fields)
                is_created = True

            # Record Verification evidence
            VerificationRecord.objects.create(
                job=job,
                status=job.verification_status,
                evidence_type=job_data.get('evidence_type', 'CAMPUS_PORTAL_VERIFIED'),
                evidence_details=job_data.get('evidence_details', 'Initial automated verification audit.'),
                is_valid=job_data.get('is_valid', True)
            )

            # Record Provenance Snapshot
            if 'raw_payload' in job_data:
                ProvenanceSnapshot.objects.create(
                    job=job,
                    raw_payload=job_data['raw_payload'],
                    http_status=200
                )

            return job, is_created
