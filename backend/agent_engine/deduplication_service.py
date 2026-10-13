import hashlib
import re
from typing import Dict, Any, Optional
from jobs.models import Job

class DuplicateDetectionService:
    """
    Identifies duplicate jobs across sources using canonical hashes,
    normalized company names, titles, and locations.
    """

    @staticmethod
    def normalize_string(val: str) -> str:
        if not val:
            return ""
        # Lowercase, strip punctuation and whitespace
        s = val.lower().strip()
        s = re.sub(r'[^a-z0-9]', '', s)
        return s

    @classmethod
    def generate_job_uid(cls, job_dict: Dict[str, Any]) -> str:
        """
        Computes a stable deterministic SHA-256 hash identifying the underlying job vacancy.
        """
        company_clean = cls.normalize_string(job_dict.get('company_name', ''))
        title_clean = cls.normalize_string(job_dict.get('title', ''))
        city_clean = cls.normalize_string(job_dict.get('city', ''))
        
        # If there's an explicit source job ID from an official source:
        source_code = job_dict.get('source_code', '')
        source_job_id = job_dict.get('source_job_id', '')

        key_components = f"{company_clean}:{title_clean}:{city_clean}"
        if source_code and source_job_id:
            key_components = f"{source_code}:{source_job_id}:{key_components}"

        return hashlib.sha256(key_components.encode('utf-8')).hexdigest()[:32]

    @classmethod
    def find_existing_job(cls, job_uid: str) -> Optional[Job]:
        """Look up by job_uid in database."""
        return Job.objects.filter(job_uid=job_uid).first()
