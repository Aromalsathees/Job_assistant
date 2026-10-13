from django.contrib import admin
from .models import Job, VerificationRecord, ProvenanceSnapshot

class VerificationRecordInline(admin.TabularInline):
    model = VerificationRecord
    extra = 0
    readonly_fields = ['checked_at']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'company_name', 'city', 'eligibility_category',
        'eligibility_classification', 'verification_status',
        'is_available', 'ranking_score', 'first_discovered_at'
    ]
    list_filter = [
        'eligibility_classification', 'eligibility_category',
        'verification_status', 'city', 'state', 'work_mode', 'is_available'
    ]
    search_fields = ['title', 'company_name', 'location', 'required_skills']
    inlines = [VerificationRecordInline]
    readonly_fields = ['job_uid', 'first_discovered_at', 'last_checked_at']

@admin.register(VerificationRecord)
class VerificationRecordAdmin(admin.ModelAdmin):
    list_display = ['job', 'status', 'evidence_type', 'checked_at', 'is_valid']
    list_filter = ['status', 'evidence_type', 'is_valid']
    search_fields = ['job__title', 'job__company_name', 'evidence_details']

@admin.register(ProvenanceSnapshot)
class ProvenanceSnapshotAdmin(admin.ModelAdmin):
    list_display = ['job', 'http_status', 'fetched_at']
    readonly_fields = ['fetched_at']
