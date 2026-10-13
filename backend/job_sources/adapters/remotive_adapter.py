import requests
import re
from typing import List, Dict, Any
from .base import BaseJobAdapter

class RemotiveAdapter(BaseJobAdapter):
    source_name = "Remotive Remote API"
    source_code = "remotive_api"
    source_type = "PUBLIC_API"
    default_trust_rating = 4

    API_URL = "https://remotive.com/api/remote-jobs"

    def fetch_raw_jobs(self, query: str = "", location: str = "", limit: int = 25) -> List[Dict[str, Any]]:
        params = {"category": "software-dev", "limit": str(limit)}
        if query:
            params["search"] = query
        try:
            resp = requests.get(self.API_URL, params=params, timeout=12, headers={"User-Agent": "SouthIndiaFresherJobAgent/1.0"})
            if resp.status_code == 200:
                data = resp.json()
                jobs = data.get("jobs", [])
                return jobs[:limit]
        except Exception:
            pass
        return []

    def normalize_record(self, raw_item: Dict[str, Any]) -> Dict[str, Any]:
        title = raw_item.get("title", "").strip()
        company = raw_item.get("company_name", "").strip()
        location_raw = raw_item.get("candidate_required_location", "Worldwide").strip()
        job_url = raw_item.get("url", "")
        description_raw = raw_item.get("description", "")
        tags = raw_item.get("tags", [])

        # Parse salary if disclosed
        salary_text = raw_item.get("salary", "").strip()
        salary_disclosed = bool(salary_text and not salary_text.lower().startswith("competitive"))

        # City / State logic
        city = "Remote"
        state = "Pan-India / Remote"
        if "india" in location_raw.lower():
            city = "Remote (India)"

        return {
            "source_job_id": str(raw_item.get("id", "")),
            "title": title,
            "company_name": company,
            "location": f"Remote - {location_raw}",
            "city": city,
            "state": state,
            "work_mode": "REMOTE",
            "employment_type": "FULL_TIME" if raw_item.get("job_type") == "full_time" else "CONTRACT",
            "experience_raw_text": "",  # Will be classified by Eligibility Agent
            "required_skills": tags if isinstance(tags, list) else [],
            "preferred_skills": [],
            "salary_disclosed": salary_disclosed,
            "salary_raw_text": salary_text,
            "salary_min": None,
            "salary_max": None,
            "salary_currency": "USD" if "$" in salary_text else "INR",
            "original_description": description_raw,
            "original_url": job_url,
            "official_apply_url": job_url,
            "posted_date": raw_item.get("publication_date"),
            "verification_status": "TRUSTED_BOARD",
            "verification_evidence_type": "JOB_BOARD_API",
            "verification_evidence_details": f"Authenticated from Remotive Public Developer API: ID {raw_item.get('id')}",
            "raw_payload": raw_item,
        }
