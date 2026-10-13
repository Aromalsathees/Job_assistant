from rest_framework import serializers
from .models import Job, VerificationRecord

class VerificationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationRecord
        fields = [
            'id', 'status', 'evidence_type', 'evidence_details',
            'checked_at', 'is_valid'
        ]


class JobSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source='source.name', read_only=True)
    source_type = serializers.CharField(source='source.source_type', read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'job_uid', 'title', 'company_name', 'location',
            'city', 'state', 'work_mode', 'employment_type',
            'experience_min_months', 'experience_max_months', 'experience_raw_text',
            'eligibility_category', 'eligibility_classification', 'eligibility_reason',
            'required_skills', 'preferred_skills', 'salary_disclosed',
            'salary_min', 'salary_max', 'salary_currency', 'salary_raw_text',
            'ai_summary', 'original_url', 'official_apply_url',
            'verification_status', 'verification_notes', 'is_available',
            'original_posted_date', 'first_discovered_at', 'last_checked_at',
            'ranking_score', 'source_name', 'source_type'
        ]


class JobDetailSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source='source.name', read_only=True)
    source_type = serializers.CharField(source='source.source_type', read_only=True)
    verification_records = VerificationRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'job_uid', 'title', 'company_name', 'location',
            'city', 'state', 'work_mode', 'employment_type',
            'experience_min_months', 'experience_max_months', 'experience_raw_text',
            'eligibility_category', 'eligibility_classification', 'eligibility_reason',
            'required_skills', 'preferred_skills', 'salary_disclosed',
            'salary_min', 'salary_max', 'salary_currency', 'salary_raw_text',
            'original_description', 'ai_summary', 'responsibilities', 'qualifications',
            'original_url', 'official_apply_url',
            'verification_status', 'verification_notes', 'is_available',
            'original_posted_date', 'first_discovered_at', 'last_checked_at',
            'ranking_score', 'source_name', 'source_type', 'verification_records'
        ]
