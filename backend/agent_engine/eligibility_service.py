import re
from typing import Dict, Any, Tuple

class EligibilityAgent:
    """
    Deterministic & rule-bound Eligibility Agent.
    Enforces STRICT 0-1 YEAR professional experience requirement for South India Freshers.
    
    Classifications:
      - ELIGIBLE_FRESHER: 0-1 year or explicitly fresher-compatible.
      - ELIGIBILITY_UNCLEAR: Missing or ambiguous experience requirements (kept out of main matching).
      - INELIGIBLE_EXPERIENCED: Requires > 1 year mandatory experience or senior title.
    """

    # Seniority keywords that immediately flag as ineligible unless explicitly marked as a student/trainee
    SENIOR_TITLE_KEYWORDS = [
        r'\bsenior\b', r'\bsr\b', r'\blead\b', r'\bprincipal\b',
        r'\bstaff\b', r'\barchitect\b', r'\bmanager\b', r'\bdirector\b',
        r'\bhead\b', r'\bvp\b', r'\btech\s*lead\b'
    ]

    # Explicit fresher indicators
    FRESHER_EXPLICIT_KEYWORDS = [
        r'\bfresher[s]?\b',
        r'\bentry[- ]level\b',
        r'\b0\s*[-–to]\s*0\s*(?:years?|yrs?)\b',
        r'\b0\s*(?:years?|yrs?)\s*(?:of)?\s*experience\b',
        r'\bno\s*experience\s*(?:required|needed)\b',
        r'\bzero\s*experience\b',
        r'\bcollege\s*grad(?:uate)?[s]?\b',
        r'\bcampus\s*hire[s]?\b',
        r'\bpassout[s]?\b',
        r'\b2024\b|\b2025\b|\b2026\b\s*batch\b',
    ]

    # Trainee keywords
    TRAINEE_KEYWORDS = [
        r'\bgraduate\s*(?:engineer|software)?\s*trainee\b',
        r'\bget\b',
        r'\bsoftware\s*trainee\b',
        r'\bengineer\s*trainee\b',
        r'\btrainee\s*software\b',
        r'\bdeveloper\s*trainee\b',
    ]

    # Internship keywords
    INTERNSHIP_KEYWORDS = [
        r'\bintern\b',
        r'\binternship\b',
        r'\bstudent\s*intern\b',
    ]

    # Explicit 0-1 year phrases
    ZERO_TO_ONE_PATTERNS = [
        r'\b0\s*[-–to]\s*1\s*(?:years?|yrs?)\b',
        r'\b0\s*[-–to]\s*12\s*months?\b',
        r'\bup\s*to\s*1\s*(?:year|yr)\b',
        r'\bup\s*to\s*12\s*months?\b',
        r'\bmaximum\s*1\s*(?:year|yr)\b',
        r'\bless\s*than\s*1\s*(?:year|yr)\b',
        r'\b1\s*year\s*or\s*less\b',
    ]

    # 0 to 6 months
    ZERO_TO_SIX_PATTERNS = [
        r'\b0\s*[-–to]\s*6\s*months?\b',
        r'\bup\s*to\s*6\s*months?\b',
        r'\bless\s*than\s*6\s*months?\b',
    ]

    # 6 to 12 months
    SIX_TO_TWELVE_PATTERNS = [
        r'\b6\s*[-–to]\s*12\s*months?\b',
        r'\b6\s*months?\s*[-–to]\s*1\s*(?:year|yr)\b',
    ]

    # Disqualifying > 1 year mandatory patterns
    EXPERIENCED_PATTERNS = [
        r'\b(?:at\s*least|min(?:imum)?|mandat(?:ory)?)\s*([2-9]|\d{2,})\s*(?:\+)?\s*(?:years?|yrs?)\b',
        r'\b([2-9]|\d{2,})\s*(?:\+)?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:mandatory|proven|relevant|hands-on|industry|commercial|professional)?\s*experience\b',
        r'\b([2-9]|\d{2,})\s*[-–to]\s*\d+\s*(?:years?|yrs?)\b',
        r'\b(?:minimum|at\s*least)\s*(?:18|24|36|48)\s*months?\b',
    ]

    def evaluate(self, job_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates a normalized job dictionary and assigns strict eligibility classification.
        """
        title = (job_dict.get('title') or '').lower()
        exp_text = (job_dict.get('experience_raw_text') or '').lower()
        desc = (job_dict.get('original_description') or '').lower()
        emp_type = (job_dict.get('employment_type') or '').upper()

        full_text = f"{title} | {exp_text} | {desc}"

        # 1. Check for disqualifying Senior/Lead Titles
        for s_pat in self.SENIOR_TITLE_KEYWORDS:
            if re.search(s_pat, title):
                # Unless it's explicitly a trainee/intern like "Trainee Lead Developer" which is rare
                return {
                    'eligibility_classification': 'INELIGIBLE_EXPERIENCED',
                    'eligibility_category': 'EXPERIENCED_OVER_1_YEAR',
                    'eligibility_reason': f"Title contains senior/lead designation matching pattern '{s_pat}'.",
                    'experience_min_months': 24,
                    'experience_max_months': 60,
                }

        # 2. Check for explicit disqualifying > 1 year mandatory requirements in experience text or description
        for pat in self.EXPERIENCED_PATTERNS:
            match = re.search(pat, exp_text) or re.search(pat, desc)
            if match:
                # Check if there is an explicit exception like "prefer 2 years but freshers may apply"
                fresher_exception = False
                for f_pat in self.FRESHER_EXPLICIT_KEYWORDS:
                    if re.search(f_pat, exp_text) or re.search(f_pat, desc):
                        fresher_exception = True
                        break
                
                if not fresher_exception:
                    return {
                        'eligibility_classification': 'INELIGIBLE_EXPERIENCED',
                        'eligibility_category': 'EXPERIENCED_OVER_1_YEAR',
                        'eligibility_reason': f"Requires >1 year mandatory experience: matched '{match.group(0)}'.",
                        'experience_min_months': 24,
                        'experience_max_months': 48,
                    }

        # 3. Check for Graduate Trainee
        for t_pat in self.TRAINEE_KEYWORDS:
            if re.search(t_pat, title) or re.search(t_pat, exp_text):
                return {
                    'eligibility_classification': 'ELIGIBLE_FRESHER',
                    'eligibility_category': 'GRADUATE_TRAINEE',
                    'eligibility_reason': "Classified as Graduate Trainee position accepting freshers.",
                    'experience_min_months': 0,
                    'experience_max_months': 12,
                }

        # 4. Check for Internships
        for i_pat in self.INTERNSHIP_KEYWORDS:
            if re.search(i_pat, title) or emp_type == 'INTERNSHIP' or re.search(i_pat, exp_text):
                return {
                    'eligibility_classification': 'ELIGIBLE_FRESHER',
                    'eligibility_category': 'INTERNSHIP_FRESHER',
                    'eligibility_reason': "Classified as Internship position accepting students / freshers.",
                    'experience_min_months': 0,
                    'experience_max_months': 6,
                }

        # 5. Check for 0-6 months explicit
        for p in self.ZERO_TO_SIX_PATTERNS:
            if re.search(p, exp_text) or re.search(p, desc):
                return {
                    'eligibility_classification': 'ELIGIBLE_FRESHER',
                    'eligibility_category': '0_6_MONTHS',
                    'eligibility_reason': f"Explicit 0–6 months requirement: matched '{p}'.",
                    'experience_min_months': 0,
                    'experience_max_months': 6,
                }

        # 6. Check for 6-12 months explicit
        for p in self.SIX_TO_TWELVE_PATTERNS:
            if re.search(p, exp_text) or re.search(p, desc):
                return {
                    'eligibility_classification': 'ELIGIBLE_FRESHER',
                    'eligibility_category': '6_12_MONTHS',
                    'eligibility_reason': f"Explicit 6–12 months requirement: matched '{p}'.",
                    'experience_min_months': 6,
                    'experience_max_months': 12,
                }

        # 7. Check for 0-1 year explicit
        for p in self.ZERO_TO_ONE_PATTERNS:
            if re.search(p, exp_text) or re.search(p, desc):
                return {
                    'eligibility_classification': 'ELIGIBLE_FRESHER',
                    'eligibility_category': '0_1_YEAR',
                    'eligibility_reason': f"Explicit 0–1 year requirement: matched '{p}'.",
                    'experience_min_months': 0,
                    'experience_max_months': 12,
                }

        # 8. Check for Fresher / 0 years explicit
        for f_pat in self.FRESHER_EXPLICIT_KEYWORDS:
            if re.search(f_pat, title) or re.search(f_pat, exp_text) or re.search(f_pat, desc):
                return {
                    'eligibility_classification': 'ELIGIBLE_FRESHER',
                    'eligibility_category': 'FRESHER_0',
                    'eligibility_reason': f"Listing explicitly welcomes Freshers / 0 years: matched '{f_pat}'.",
                    'experience_min_months': 0,
                    'experience_max_months': 0,
                }

        # 9. Important rule: "Do not infer fresher eligibility from the word 'Junior' alone."
        # If experience is completely unstated or missing:
        # "A job missing experience information must be classified as 'Eligibility Unclear' and kept out of the default matching results."
        return {
            'eligibility_classification': 'ELIGIBILITY_UNCLEAR',
            'eligibility_category': 'UNCLEAR',
            'eligibility_reason': "Experience requirements not explicitly stated. Kept out of default matching results.",
            'experience_min_months': 0,
            'experience_max_months': 12,
        }
