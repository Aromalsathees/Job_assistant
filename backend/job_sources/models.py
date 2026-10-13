from django.db import models

class JobSource(models.Model):
    SOURCE_TYPES = [
        ('OFFICIAL_PORTAL', 'Official IT Park / Campus Portal'),
        ('DIRECT_EMPLOYER', 'Direct Verified Employer Page'),
        ('PUBLIC_API', 'Permitted Public Job-Board API'),
        ('COMMUNITY_FEED', 'Authorized Industry RSS Feed'),
    ]

    name = models.CharField(max_length=150, unique=True)
    code = models.SlugField(max_length=80, unique=True)
    source_type = models.CharField(max_length=30, choices=SOURCE_TYPES, default='PUBLIC_API')
    base_url = models.URLField(max_length=500)
    is_active = models.BooleanField(default=True)
    trust_rating = models.IntegerField(default=4, help_text="1 to 5 trust scale")
    last_polled_at = models.DateTimeField(null=True, blank=True)
    total_jobs_found = models.IntegerField(default=0)
    config = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-trust_rating', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_source_type_display()})"
