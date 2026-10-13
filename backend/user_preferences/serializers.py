from rest_framework import serializers
from .models import UserPreference

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = [
            'id', 'client_session_id', 'target_roles', 'target_locations',
            'preferred_skills', 'preferred_work_modes', 'min_salary',
            'notification_email', 'daily_schedule_enabled', 'schedule_hour',
            'schedule_timezone', 'created_at', 'updated_at'
        ]
