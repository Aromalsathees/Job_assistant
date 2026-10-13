from datetime import timedelta
from django.utils import timezone
from typing import Dict, Any, List
from jobs.models import Job

class DailyReportingService:
    """
    Generates structured daily intelligence reports of genuine fresher IT jobs
    discovered across Kerala and South India.
    """

    @classmethod
    def generate_daily_digest(cls) -> Dict[str, Any]:
        now = timezone.now()
        yesterday = now - timedelta(hours=24)

        new_jobs = Job.objects.filter(
            eligibility_classification='ELIGIBLE_FRESHER',
            is_available=True,
            first_discovered_at__gte=yesterday
        ).order_by('-ranking_score', '-first_discovered_at')

        total_new = new_jobs.count()
        official_verified = new_jobs.filter(verification_status='OFFICIAL_VERIFIED').count()
        trusted_boards = new_jobs.filter(verification_status='TRUSTED_BOARD').count()

        kerala_jobs = new_jobs.filter(state='Kerala')
        tamil_nadu_jobs = new_jobs.filter(state='Tamil Nadu')
        remote_jobs = new_jobs.filter(work_mode='REMOTE')

        top_openings = []
        for j in new_jobs[:5]:
            top_openings.append({
                'title': j.title,
                'company': j.company_name,
                'city': j.city,
                'skills': j.required_skills[:4],
                'salary': j.salary_raw_text or 'Undisclosed',
                'url': j.original_url,
                'verification': j.get_verification_status_display()
            })

        text_summary = (
            f"Daily Fresher Job Intelligence Briefing - {now.strftime('%d %b %Y')}\n"
            f"==========================================================\n"
            f"• Newly Discovered Eligible Jobs: {total_new}\n"
            f"• Official Source Verified: {official_verified}\n"
            f"• Kerala Campus Jobs: {kerala_jobs.count()}\n"
            f"• Tamil Nadu Opportunities: {tamil_nadu_jobs.count()}\n"
            f"• Remote Jobs: {remote_jobs.count()}\n"
            f"\nTop High-Relevance Openings:\n"
        )
        for idx, o in enumerate(top_openings, 1):
            text_summary += f"{idx}. {o['title']} @ {o['company']} ({o['city']}) - [{o['verification']}]\n"

        return {
            'report_date': now.isoformat(),
            'total_new_eligible': total_new,
            'official_verified_count': official_verified,
            'trusted_boards_count': trusted_boards,
            'kerala_count': kerala_jobs.count(),
            'tamil_nadu_count': tamil_nadu_jobs.count(),
            'remote_count': remote_jobs.count(),
            'top_openings': top_openings,
            'text_digest': text_summary,
        }
