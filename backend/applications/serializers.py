from rest_framework import serializers
from .models import SavedJob, JobApplication
from jobs.serializers import JobSerializer

class SavedJobSerializer(serializers.ModelSerializer):
    job_details = JobSerializer(source='job', read_only=True)

    class Meta:
        model = SavedJob
        fields = ['id', 'client_session_id', 'job', 'job_details', 'notes', 'saved_at']


class JobApplicationSerializer(serializers.ModelSerializer):
    job_details = JobSerializer(source='job', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = JobApplication
        fields = [
            'id', 'client_session_id', 'job', 'job_details', 'status',
            'status_display', 'applied_date', 'resume_version',
            'interview_date', 'notes', 'created_at', 'updated_at'
        ]
