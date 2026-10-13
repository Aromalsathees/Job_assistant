from langchain_core.tools import tool
from jobs.models import Job

@tool
def job_details_tool(job_id: int) -> dict:
    """Fetch complete details of a job using its database ID."""

    try:
        job = Job.objects.get(id=job_id)

        return {
            "id": job.id,
            "job_uid": job.job_uid,
            "title": job.title,
            "company_name": job.company_name,
            "location": job.location,
            "city": job.city,
            "state": job.state,
            "work_mode": job.work_mode,
            "employment_type": job.employment_type,

            "experience_min_months": job.experience_min_months,
            "experience_max_months": job.experience_max_months,
            "experience_raw_text": job.experience_raw_text,
            "eligibility_category": job.eligibility_category,
            "eligibility_classification": (
                job.eligibility_classification
            ),

            "eligibility_reason": job.eligibility_reason,

            "required_skills": job.required_skills,
            "preferred_skills": job.preferred_skills,

            "salary_disclosed": job.salary_disclosed,
            "salary_min": (
                str(job.salary_min)
                if job.salary_min is not None else None
            ),
            "salary_max": (
                str(job.salary_max)
                if job.salary_max is not None else None
            ),
            "salary_currency": job.salary_currency,
            "salary_raw_text": job.salary_raw_text,

            "original_description": job.original_description,
            "ai_summary": job.ai_summary,
            "responsibilities": job.responsibilities,
            "qualifications": job.qualifications,

            "original_url": job.original_url,
            "official_apply_url": job.official_apply_url,

            "verification_status": job.verification_status,
            "verification_notes": job.verification_notes,
            "is_available": job.is_available,

            "original_posted_date": (
                job.original_posted_date.isoformat()
                if job.original_posted_date else None
            ),
            "ranking_score": job.ranking_score,
        }

    except Job.DoesNotExist:
        return {"error": f"Job with ID {job_id} was not found."}


@tool
def verified_record_tool(job_id: int) -> dict:
    """Fetch verification records for a job using its database ID."""

    records = VerificationRecord.objects.filter(
        job_id=job_id
    ).order_by("-checked_at")

    if not records.exists():
        return {
            "job_id": job_id,
            "message": "No verification records found for this job.",
            "verification_records": [],
        }

    verification_records = []

    for record in records:
        verification_records.append({
            "id": record.id,
            "job_id": record.job_id,
            "job_title": record.job.title,
            "status": record.status,
            "evidence_type": record.evidence_type,
            "evidence_details": record.evidence_details,
            "checked_at": (
                record.checked_at.isoformat()
                if record.checked_at else None
            ),
            "is_valid": record.is_valid,
        })

    return {
        "job_id": job_id,
        "job_title": records.first().job.title,
        "total_records": len(verification_records),
        "verification_records": verification_records,
    }
