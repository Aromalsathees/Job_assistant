import uuid
from django.db import models

class DiscoveryRun(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('SUCCESS', 'Success'),
        ('PARTIAL_SUCCESS', 'Partial Success'),
        ('FAILED', 'Failed'),
    ]

    run_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', db_index=True)
    started_at = models.DateTimeField(auto_now_add=True, db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.FloatField(default=0.0)

    # Auditing metrics
    sources_checked = models.JSONField(default=list, blank=True)
    sources_failed = models.JSONField(default=list, blank=True)
    jobs_discovered = models.IntegerField(default=0)
    jobs_updated = models.IntegerField(default=0)
    duplicates_skipped = models.IntegerField(default=0)
    ineligible_excluded = models.IntegerField(default=0)
    unclear_separated = models.IntegerField(default=0)
    official_verified_count = models.IntegerField(default=0)
    trusted_board_count = models.IntegerField(default=0)

    summary_notes = models.TextField(blank=True)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"DiscoveryRun {self.run_id} [{self.status}] at {self.started_at}"
