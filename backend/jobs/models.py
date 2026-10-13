import uuid
from django.db import models

class Job(models.Model):
    # Eligibility classifications
    ELIGIBILITY_CLASSIFICATIONS = [
        ('ELIGIBLE_FRESHER', 'Eligible Fresher (0-1 Year)'),
        ('ELIGIBILITY_UNCLEAR', 'Eligibility Unclear'),
        ('INELIGIBLE_EXPERIENCED', 'Ineligible Experienced (>1 Year)'),
    ]

    # Detailed Category
    ELIGIBILITY_CATEGORIES = [
        ('FRESHER_0', 'Fresher / 0 years'),
        ('0_6_MONTHS', '0–6 months'),
        ('6_12_MONTHS', '6–12 months'),
        ('0_1_YEAR', '0–1 year'),
        ('GRADUATE_TRAINEE', 'Graduate Trainee'),
        ('INTERNSHIP_FRESHER', 'Internship (Fresher Eligible)'),
        ('EXPERIENCED_OVER_1_YEAR', 'Experienced (> 1 Year)'),
        ('UNCLEAR', 'Experience Unclear'),
    ]

    # Verification status
    VERIFICATION_STATUSES = [
        ('OFFICIAL_VERIFIED', 'Official source verified'),
        ('TRUSTED_BOARD', 'Trusted job-board listing'),
        ('NEEDS_VERIFICATION', 'Needs verification'),
        ('EXPIRED', 'Expired or unavailable'),
        ('SUSPICIOUS', 'Suspicious'),
    ]

    # Work mode
    WORK_MODES = [
        ('ONSITE', 'On-site'),
        ('HYBRID', 'Hybrid'),
        ('REMOTE', 'Remote'),
    ]

    # Employment types
    EMPLOYMENT_TYPES = [
        ('FULL_TIME', 'Full-time'),
        ('INTERNSHIP', 'Internship'),
        ('CONTRACT', 'Contract'),
        ('TRAINEE', 'Trainee'),
    ]

    # Identification & deduplication
    job_uid = models.CharField(max_length=64, unique=True, db_index=True)
    source = models.ForeignKey(
        'job_sources.JobSource',
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    source_job_id = models.CharField(max_length=255, blank=True, db_index=True)

    # Core attributes
    title = models.CharField(max_length=255, db_index=True)
    company_name = models.CharField(max_length=255, db_index=True)
    location = models.CharField(max_length=255)
    city = models.CharField(max_length=100, db_index=True)
    state = models.CharField(max_length=100, default='Kerala')
    work_mode = models.CharField(max_length=20, choices=WORK_MODES, default='ONSITE')
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES, default='FULL_TIME')

    # Strict Experience Classification
    experience_min_months = models.IntegerField(default=0)
    experience_max_months = models.IntegerField(default=12)
    experience_raw_text = models.CharField(max_length=255, blank=True)
    eligibility_category = models.CharField(
        max_length=30,
        choices=ELIGIBILITY_CATEGORIES,
        default='0_1_YEAR'
    )
    eligibility_classification = models.CharField(
        max_length=30,
        choices=ELIGIBILITY_CLASSIFICATIONS,
        default='ELIGIBLE_FRESHER',
        db_index=True
    )
    eligibility_reason = models.TextField(blank=True)

    # Skills & compensation
    required_skills = models.JSONField(default=list, blank=True)
    preferred_skills = models.JSONField(default=list, blank=True)
    salary_disclosed = models.BooleanField(default=False)
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=10, default='INR')
    salary_raw_text = models.CharField(max_length=255, blank=True)

    # Content
    original_description = models.TextField(help_text="Verbatim original job description")
    ai_summary = models.TextField(blank=True, help_text="AI-generated summary (clearly separated)")
    responsibilities = models.JSONField(default=list, blank=True)
    qualifications = models.JSONField(default=list, blank=True)

    # URLs
    original_url = models.URLField(max_length=1000)
    official_apply_url = models.URLField(max_length=1000, blank=True)

    # Verification
    verification_status = models.CharField(
        max_length=30,
        choices=VERIFICATION_STATUSES,
        default='NEEDS_VERIFICATION',
        db_index=True
    )
    verification_notes = models.TextField(blank=True)
    is_available = models.BooleanField(default=True, db_index=True)

    # Timestamps & Ranking
    original_posted_date = models.DateTimeField(null=True, blank=True)
    first_discovered_at = models.DateTimeField(auto_now_add=True, db_index=True)
    last_checked_at = models.DateTimeField(auto_now=True)
    ranking_score = models.FloatField(default=0.0, db_index=True)

    class Meta:
        ordering = ['-ranking_score', '-first_discovered_at']
        indexes = [
            models.Index(fields=['eligibility_classification', 'is_available']),
            models.Index(fields=['city', 'state']),
            models.Index(fields=['verification_status']),
            models.Index(fields=['company_name']),
        ]

    def __str__(self):
        return f"{self.title} @ {self.company_name} ({self.city}) [{self.eligibility_classification}]"


class VerificationRecord(models.Model):
    EVIDENCE_TYPES = [
        ('OFFICIAL_DOMAIN_MATCH', 'Official company domain match'),
        ('CAMPUS_PORTAL_VERIFIED', 'IT Park official listing verified'),
        ('JOB_BOARD_API', 'Verified public job-board API'),
        ('DIRECT_CAREERS_LINK', 'Direct company careers portal application link'),
        ('SUSPICIOUS_FEE_FLAG', 'Suspicious monetary fee request or security deposit'),
        ('SUSPICIOUS_COMPANY_FLAG', 'Potential company impersonation detected'),
        ('HTTP_404_EXPIRED', 'Listing URL not accessible / expired'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='verification_records')
    status = models.CharField(max_length=30, choices=Job.VERIFICATION_STATUSES)
    evidence_type = models.CharField(max_length=40, choices=EVIDENCE_TYPES)
    evidence_details = models.TextField()
    checked_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    class Meta:
        ordering = ['-checked_at']

    def __str__(self):
        return f"Verification for {self.job.title} - {self.status} ({self.evidence_type})"


class ProvenanceSnapshot(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='snapshots')
    raw_payload = models.JSONField()
    http_status = models.IntegerField(default=200)
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Snapshot for {self.job.id} at {self.fetched_at}"
