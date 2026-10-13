from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from agent_engine.reporting_service import DailyReportingService

@api_view(['GET'])
def daily_digest_api(request):
    """Returns today's fresher job intelligence briefing."""
    digest = DailyReportingService.generate_daily_digest()
    return Response(digest)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Core Domain APIs
    path('api/', include('jobs.urls')),
    path('api/', include('job_sources.urls')),
    path('api/', include('discovery_runs.urls')),
    path('api/', include('applications.urls')),
    path('api/', include('user_preferences.urls')),
    path('api/daily-digest/', daily_digest_api, name='daily-digest'),
]
