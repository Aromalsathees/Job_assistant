from datetime import datetime
from django.utils import timezone
from typing import Dict, Any

class RankingService:
    """
    Computes ranking score prioritizing South India & Kerala fresher IT jobs.
    Default highest priority: Kerala (Ernakulam/Kochi/Infopark & Thiruvananthapuram/Technopark).
    """

    KERALA_TOP_PRIORITY_CITIES = [
        'kochi', 'ernakulam', 'kakkanad', 'infopark',
        'thiruvananthapuram', 'trivandrum', 'technopark',
        'kozhikode', 'thrissur', 'cherthala', 'kerala'
    ]

    TAMIL_NADU_CITIES = ['chennai', 'coimbatore', 'madurai', 'trichy', 'tamil nadu']
    OTHER_SOUTH_CITIES = ['bengaluru', 'bangalore', 'hyderabad', 'mysuru', 'mysore']

    KEY_ROLES_KEYWORDS = [
        'python', 'django', 'fastapi', 'ai agent', 'agentic',
        'generative ai', 'llm', 'rag', 'langchain', 'langgraph',
        'full stack', 'backend', 'trainee', 'fresher'
    ]

    @classmethod
    def calculate_score(cls, job_dict: Dict[str, Any]) -> float:
        score = 0.0

        # 1. Eligibility priority
        eligibility = job_dict.get('eligibility_classification', '')
        if eligibility == 'ELIGIBLE_FRESHER':
            score += 50.0
            category = job_dict.get('eligibility_category', '')
            if category in ('FRESHER_0', '0_6_MONTHS'):
                score += 10.0
        elif eligibility == 'ELIGIBILITY_UNCLEAR':
            score += 10.0
        else:
            return 0.0  # Ineligible roles get lowest rank

        # 2. Location priority (Kerala & Kochi highest default priority)
        city = (job_dict.get('city') or '').lower()
        location = (job_dict.get('location') or '').lower()
        state = (job_dict.get('state') or '').lower()
        loc_text = f"{city} {location} {state}"

        if any(c in loc_text for c in ['kochi', 'ernakulam', 'kakkanad', 'infopark']):
            score += 40.0
        elif any(c in loc_text for c in cls.KERALA_TOP_PRIORITY_CITIES):
            score += 35.0
        elif any(c in loc_text for c in cls.TAMIL_NADU_CITIES):
            score += 25.0
        elif 'remote' in loc_text or job_dict.get('work_mode') == 'REMOTE':
            score += 25.0
        elif any(c in loc_text for c in cls.OTHER_SOUTH_CITIES):
            score += 20.0
        else:
            score += 10.0

        # 3. Verification status priority
        v_status = job_dict.get('verification_status', '')
        if v_status == 'OFFICIAL_VERIFIED':
            score += 25.0
        elif v_status == 'TRUSTED_BOARD':
            score += 15.0
        elif v_status == 'NEEDS_VERIFICATION':
            score += 5.0
        elif v_status == 'SUSPICIOUS':
            score -= 100.0

        # 4. Target role relevance
        title = (job_dict.get('title') or '').lower()
        skills = " ".join([str(s).lower() for s in job_dict.get('required_skills', [])])
        role_text = f"{title} {skills}"

        for kw in cls.KEY_ROLES_KEYWORDS:
            if kw in role_text:
                score += 5.0

        # 5. Salary disclosed bonus (transparency)
        if job_dict.get('salary_disclosed'):
            score += 5.0

        return round(score, 2)
