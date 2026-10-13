from rest_framework import serializers
from .models import JobSource

class JobSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSource
        fields = [
            'id', 'name', 'code', 'source_type', 'base_url',
            'is_active', 'trust_rating', 'last_polled_at',
            'total_jobs_found', 'created_at'
        ]
