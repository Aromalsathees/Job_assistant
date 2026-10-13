from rest_framework import serializers
from .models import DiscoveryRun

class DiscoveryRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscoveryRun
        fields = [
            'id', 'run_id', 'status', 'started_at', 'completed_at',
            'duration_seconds', 'sources_checked', 'sources_failed',
            'jobs_discovered', 'jobs_updated', 'duplicates_skipped',
            'ineligible_excluded', 'unclear_separated',
            'official_verified_count', 'trusted_board_count',
            'summary_notes', 'error_message'
        ]
