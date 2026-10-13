from django.db import models
from django.contrib.auth import get_user_model
from jobs.models import Job

User = get_user_model()

class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='saved_jobs')
    client_session_id = models.CharField(max_length=100, default='default-user', db_index=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by_users')
    notes = models.TextField(blank=True)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-saved_at']
        unique_together = ('client_session_id', 'job')

    def __str__(self):
        return f"Saved: {self.job.title} by {self.client_session_id}"


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('INTERESTED', 'Interested'),
        ('TO_APPLY', 'To Apply'),
        ('APPLIED', 'Applied'),
        ('ASSESSMENT', 'Assessment Scheduled'),
        ('INTERVIEW', 'Interview'),
        ('OFFER', 'Offer Received'),
        ('REJECTED', 'Rejected'),
        ('WITHDRAWN', 'Withdrawn'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='job_applications')
    client_session_id = models.CharField(max_length=100, default='default-user', db_index=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='INTERESTED', db_index=True)
    applied_date = models.DateField(null=True, blank=True)
    resume_version = models.CharField(max_length=100, blank=True)
    interview_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        unique_together = ('client_session_id', 'job')

    def __str__(self):
        return f"Application: {self.job.title} @ {self.job.company_name} [{self.status}]"
