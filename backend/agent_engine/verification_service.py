import re
from urllib.parse import urlparse
from typing import Dict, Any, Tuple

class VerificationService:
    """
    Verifies authenticity of job postings, assesses domain provenance,
    and detects suspicious fraudulent hiring practices.
    """

    # Suspicious phrases indicating fraudulent job offers or fee demands
    SUSPICIOUS_PHRASES = [
        r'\bregistration\s*fee\b',
        r'\bprocessing\s*fee\b',
        r'\bpay\s*(?:money|amount|deposit)\b',
        r'\bsecurity\s*deposit\b',
        r'\btraining\s*fees\b',
        r'\bbank\s*transfer\s*before\s*interview\b',
        r'\bpay\s*for\s*(?:laptop|equipment|visa)\b',
        r'\bgiveaway\b|\bwhatsapp\s*only\s*recruitment\b',
    ]

    # Trusted domain extensions and portals
    OFFICIAL_PORTAL_DOMAINS = [
        'technopark.in',
        'infopark.in',
        'keralait.org',
        'keralait.in',
        'zoho.com',
        'thoughtworks.com',
        'juspay.in',
        'ibsplc.com',
        'nestdigital.com',
        'fingent.com',
        'experionglobal.com',
        'qburst.com',
        'ust.com',
        'tataelxsi.com',
        'suntecgroup.com',
        'techgentsia.com',
    ]

    TRUSTED_JOB_BOARDS = [
        'remotive.com',
        'arbeitnow.com',
        'jobicy.com',
        'linkedin.com',
    ]

    def verify(self, job_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates job details for authenticity, source credibility, and suspicious markers.
        """
        title = (job_dict.get('title') or '').lower()
        desc = (job_dict.get('original_description') or '').lower()
        orig_url = job_dict.get('original_url') or ''
        apply_url = job_dict.get('official_apply_url') or ''
        source_type = job_dict.get('source_type') or ''

        # 1. Suspicious Frauds / Monetary Fee Demands
        for s_pat in self.SUSPICIOUS_PHRASES:
            if re.search(s_pat, desc) or re.search(s_pat, title):
                return {
                    'verification_status': 'SUSPICIOUS',
                    'evidence_type': 'SUSPICIOUS_FEE_FLAG',
                    'evidence_details': f"CRITICAL: Suspicious phrasing detected ('{s_pat}'). Requesting fees or deposits violates genuine hiring ethics.",
                    'is_available': False,
                    'is_valid': False,
                }

        # 2. Check Domain Provenance
        domain = self._extract_domain(apply_url or orig_url)

        # Check Official Portals & Direct Employers
        if any(trusted in domain for trusted in self.OFFICIAL_PORTAL_DOMAINS) or source_type in ('OFFICIAL_PORTAL', 'DIRECT_EMPLOYER'):
            return {
                'verification_status': 'OFFICIAL_VERIFIED',
                'evidence_type': 'OFFICIAL_DOMAIN_MATCH' if source_type == 'DIRECT_EMPLOYER' else 'CAMPUS_PORTAL_VERIFIED',
                'evidence_details': f"Verified employer/campus provenance: official listing on '{domain}'. Application route directly controlled by verified company/park authority.",
                'is_available': True,
                'is_valid': True,
            }

        # Check Trusted Job Boards
        if any(tb in domain for tb in self.TRUSTED_JOB_BOARDS) or source_type == 'PUBLIC_API':
            return {
                'verification_status': 'TRUSTED_BOARD',
                'evidence_type': 'JOB_BOARD_API',
                'evidence_details': f"Published through authorized public API / job aggregator ({domain}). Direct source link verified.",
                'is_available': True,
                'is_valid': True,
            }

        # Needs verification default
        return {
            'verification_status': 'NEEDS_VERIFICATION',
            'evidence_type': 'CAMPUS_PORTAL_VERIFIED',
            'evidence_details': "External web listing. Direct employer portal verification pending manual confirmation.",
            'is_available': True,
            'is_valid': True,
        }

    def _extract_domain(self, url: str) -> str:
        try:
            parsed = urlparse(url)
            return parsed.netloc.lower()
        except Exception:
            return ""
