from rest_framework import viewsets
from .models import JobSource
from .serializers import JobSourceSerializer

class JobSourceViewSet(viewsets.ReadOnlyModelViewSet):
    """View active and configured job sources."""
    queryset = JobSource.objects.all().order_by('-trust_rating', 'name')
    serializer_class = JobSourceSerializer
