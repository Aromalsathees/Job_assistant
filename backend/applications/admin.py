from django.contrib import admin
from .models import SavedJob, JobApplication

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ['client_session_id', 'job', 'saved_at']
    search_fields = ['client_session_id', 'job__title', 'job__company_name']

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['client_session_id', 'job', 'status', 'applied_date', 'updated_at']
    list_filter = ['status', 'applied_date']
    search_fields = ['client_session_id', 'job__title', 'job__company_name', 'notes']
