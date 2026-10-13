import requests
from typing import List, Dict, Any
from .base import BaseJobAdapter

class ArbeitnowAdapter(BaseJobAdapter):
    source_name = "Arbeitnow Job Board API"
    source_code = "arbeitnow_api"
    source_type = "PUBLIC_API"
    default_trust_rating = 4

    API_URL = "https://www.arbeitnow.com/api/job-board-api"

    def fetch_raw_jobs(self, query: str = "", location: str = "", limit: int = 25) -> List[Dict[str, Any]]:
        try:
            resp = requests.get(
                self.API_URL,
                timeout=12,
                headers={"User-Agent": "SouthIndiaFresherJobAgent/1.0"}
            )
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("data", [])
                return items[:limit]
        except Exception:
            pass
        return []

    def normalize_record(self, raw_item: Dict[str, Any]) -> Dict[str, Any]:
        title = raw_item.get("title", "").strip()
        company = raw_item.get("company_name", "").strip()
        location_raw = raw_item.get("location", "Remote").strip()
        url = raw_item.get("url", "")
        desc = raw_item.get("description", "")
        tags = raw_item.get("tags", [])
        is_remote = raw_item.get("remote", False)

        work_mode = "REMOTE" if is_remote else "ONSITE"
        city = "Remote" if is_remote else location_raw

        return {
            "source_job_id": raw_item.get("slug", ""),
            "title": title,
            "company_name": company,
            "location": location_raw,
            "city": city,
            "state": "Pan-India / Remote" if is_remote else "International",
            "work_mode": work_mode,
            "employment_type": "FULL_TIME",
            "experience_raw_text": "",
            "required_skills": tags if isinstance(tags, list) else [],
            "preferred_skills": [],
            "salary_disclosed": False,
            "salary_raw_text": "",
            "salary_min": None,
            "salary_max": None,
            "salary_currency": "EUR",
            "original_description": desc,
            "original_url": url,
            "official_apply_url": url,
            "posted_date": None,
            "verification_status": "TRUSTED_BOARD",
            "verification_evidence_type": "JOB_BOARD_API",
            "verification_evidence_details": f"Discovered via Arbeitnow Authorized Public API (Slug: {raw_item.get('slug')})",
            "raw_payload": raw_item,
        }
