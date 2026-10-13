from django.contrib import admin
from .models import DiscoveryRun

@admin.register(DiscoveryRun)
class DiscoveryRunAdmin(admin.ModelAdmin):
    list_display = [
        'run_id', 'status', 'started_at', 'duration_seconds',
        'jobs_discovered', 'jobs_updated', 'ineligible_excluded',
        'official_verified_count'
    ]
    list_filter = ['status', 'started_at']
    search_fields = ['run_id', 'summary_notes', 'error_message']
    readonly_fields = ['run_id', 'started_at', 'completed_at']
