from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import DiscoveryRun
from .serializers import DiscoveryRunSerializer
from agent_engine.orchestrator import JobAgentOrchestrator

class DiscoveryRunViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoints for inspecting discovery run history, audit logs,
    and triggering automated or on-demand discovery sweeps.
    """
    queryset = DiscoveryRun.objects.all().order_by('-started_at')
    serializer_class = DiscoveryRunSerializer

    @action(detail=False, methods=['post'], url_path='trigger')
    def trigger_discovery(self, request):
        """
        Executes on-demand discovery across active sources with strict eligibility rules.
        """
        # Check if an existing run is currently active
        running = DiscoveryRun.objects.filter(status='RUNNING').first()
        if running:
            return Response({
                'message': 'A discovery run is already in progress.',
                'run_id': str(running.run_id),
                'status': 'RUNNING',
            }, status=status.HTTP_409_CONFLICT)

        try:
            orchestrator = JobAgentOrchestrator()
            run_instance = orchestrator.run_discovery()
            serializer = self.get_serializer(run_instance)
            return Response({
                'message': 'Discovery executed successfully.',
                'run': serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'error': f'Discovery failed to complete: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='latest-summary')
    def latest_summary(self, request):
        """Returns the most recent successful discovery execution and verification totals."""
        latest_success = DiscoveryRun.objects.filter(status__in=['SUCCESS', 'PARTIAL_SUCCESS']).first()
        serializer = self.get_serializer(latest_success) if latest_success else None
        return Response({
            'last_successful_run': serializer.data if serializer else None,
            'total_runs_count': DiscoveryRun.objects.count(),
        })
