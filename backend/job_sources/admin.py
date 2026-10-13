from django.contrib import admin
from .models import JobSource

@admin.register(JobSource)
class JobSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'source_type', 'is_active', 'trust_rating', 'total_jobs_found', 'last_polled_at']
    list_filter = ['source_type', 'is_active', 'trust_rating']
    search_fields = ['name', 'code', 'base_url']
