from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import SavedJob, JobApplication
from .serializers import SavedJobSerializer, JobApplicationSerializer

class SavedJobViewSet(viewsets.ModelViewSet):
    """
    CRUD API for saving and bookmarking jobs.
    Supports client_session_id header or query param.
    """
    serializer_class = SavedJobSerializer

    def get_queryset(self):
        session_id = self.request.headers.get('X-Client-Session', 'default-user')
        return SavedJob.objects.filter(client_session_id=session_id).select_related('job', 'job__source')

    def perform_create(self, serializer):
        session_id = self.request.headers.get('X-Client-Session', 'default-user')
        serializer.save(client_session_id=session_id)


class JobApplicationViewSet(viewsets.ModelViewSet):
    """
    Application tracker API supporting statuses:
    INTERESTED, TO_APPLY, APPLIED, ASSESSMENT, INTERVIEW, OFFER, REJECTED, WITHDRAWN.
    """
    serializer_class = JobApplicationSerializer

    def get_queryset(self):
        session_id = self.request.headers.get('X-Client-Session', 'default-user')
        return JobApplication.objects.filter(client_session_id=session_id).select_related('job', 'job__source')

    def perform_create(self, serializer):
        session_id = self.request.headers.get('X-Client-Session', 'default-user')
        serializer.save(client_session_id=session_id)
