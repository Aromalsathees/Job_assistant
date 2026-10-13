import re
from typing import Dict, Any, List

class NormalizationService:
    """
    Normalizes raw job listings into the strict unified job schema.
    Extracts skills, cleans descriptions, and generates structured disclaimed summaries.
    """

    KNOWN_TECH_SKILLS = [
        "Python", "Django", "FastAPI", "Flask", "React", "JavaScript",
        "TypeScript", "HTML", "CSS", "Tailwind CSS", "PostgreSQL",
        "MySQL", "MongoDB", "Redis", "SQLite", "Docker", "Kubernetes",
        "AWS", "Azure", "GCP", "Git", "GitHub", "Linux", "REST APIs",
        "GraphQL", "Celery", "Pandas", "NumPy", "LangChain", "LangGraph",
        "LlamaIndex", "ChromaDB", "Pinecone", "RAG", "Agentic AI",
        "Prompt Engineering", "OpenAI", "Hugging Face", "PyTest",
        "CI/CD", "Machine Learning", "NLP"
    ]

    @classmethod
    def normalize(cls, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Ensures all standard keys are present, types sanitized, and null-safe."""
        title = (raw.get('title') or '').strip()
        company = (raw.get('company_name') or '').strip()
        location = (raw.get('location') or '').strip()
        city = (raw.get('city') or 'Kochi').strip()
        state = (raw.get('state') or 'Kerala').strip()
        work_mode = (raw.get('work_mode') or 'ONSITE').upper()
        if work_mode not in ('ONSITE', 'HYBRID', 'REMOTE'):
            work_mode = 'ONSITE'

        emp_type = (raw.get('employment_type') or 'FULL_TIME').upper()
        if emp_type not in ('FULL_TIME', 'INTERNSHIP', 'CONTRACT', 'TRAINEE'):
            emp_type = 'FULL_TIME'

        desc = raw.get('original_description') or ''
        # Strip dangerous tags but keep readable structure
        cleaned_desc = re.sub(r'<script.*?>.*?</script>', '', desc, flags=re.DOTALL | re.IGNORECASE)

        # Extract skills if not provided
        req_skills = raw.get('required_skills') or []
        if not req_skills:
            req_skills = cls._extract_skills(f"{title} {cleaned_desc}")

        # Structured AI summary with explicit disclaimer
        ai_summary = cls._generate_summary(title, company, city, req_skills, raw.get('experience_raw_text', ''))

        return {
            'source_job_id': str(raw.get('source_job_id') or ''),
            'title': title,
            'company_name': company,
            'location': location or city,
            'city': city,
            'state': state,
            'work_mode': work_mode,
            'employment_type': emp_type,
            'experience_raw_text': (raw.get('experience_raw_text') or '').strip(),
            'required_skills': req_skills,
            'preferred_skills': raw.get('preferred_skills') or [],
            'salary_disclosed': bool(raw.get('salary_disclosed')),
            'salary_raw_text': (raw.get('salary_raw_text') or '').strip(),
            'salary_min': raw.get('salary_min'),
            'salary_max': raw_item_get_salary(raw.get('salary_max')),
            'salary_currency': raw.get('salary_currency') or 'INR',
            'original_description': cleaned_desc,
            'ai_summary': ai_summary,
            'original_url': raw.get('original_url') or '',
            'official_apply_url': raw.get('official_apply_url') or raw.get('original_url') or '',
            'posted_date': raw.get('posted_date'),
            'verification_status': raw.get('verification_status') or 'NEEDS_VERIFICATION',
            'verification_evidence_type': raw.get('verification_evidence_type') or 'CAMPUS_PORTAL_VERIFIED',
            'verification_evidence_details': raw.get('verification_evidence_details') or '',
            'raw_payload': raw.get('raw_payload') or raw,
        }

    @classmethod
    def _extract_skills(cls, text: str) -> List[str]:
        found = []
        text_lower = text.lower()
        for skill in cls.KNOWN_TECH_SKILLS:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found.append(skill)
        return found[:10]

    @classmethod
    def _generate_summary(cls, title: str, company: str, city: str, skills: List[str], exp_text: str) -> str:
        skills_str = ", ".join(skills[:5]) if skills else "Core software engineering fundamentals"
        exp_info = f"Experience context: {exp_text}." if exp_text else "Experience context: Entry level / Fresher friendly."
        return (
            f"[AI Summary - Disclaimed]: {title} opportunity at {company} located in {city}. "
            f"Focus areas include {skills_str}. {exp_info} "
            f"Always refer to the verbatim Original Job Description below for official employer terms."
        )

def raw_item_get_salary(val):
    if val is None or val == '':
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None
