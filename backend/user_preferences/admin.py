from django.contrib import admin
from .models import UserPreference

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['client_session_id', 'daily_schedule_enabled', 'schedule_hour', 'updated_at']
    search_fields = ['client_session_id', 'notification_email']
