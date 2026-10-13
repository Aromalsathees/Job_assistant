from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Job, VerificationRecord
from .serializers import JobSerializer, JobDetailSerializer, VerificationRecordSerializer
from .filters import JobFilter
from discovery_runs.models import DiscoveryRun

class JobViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for discovering and filtering genuine fresher IT jobs.
    Strictly filters for 0-1 year of professional experience by default.
    """
    filterset_class = JobFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'company_name', 'location', 'city']
    ordering_fields = ['ranking_score', 'first_discovered_at', 'salary_min']
    ordering = ['-ranking_score', '-first_discovered_at']

    def get_queryset(self):
        # Base queryset - active listings
        qs = Job.objects.filter(is_available=True).select_related('source')

        # Check explicit eligibility parameter
        eligibility = self.request.query_params.get('eligibility', '').upper()
        if eligibility == 'ALL':
            return qs
        elif eligibility in ('UNCLEAR', 'ELIGIBILITY_UNCLEAR'):
            return qs.filter(eligibility_classification='ELIGIBILITY_UNCLEAR')
        elif eligibility in ('INELIGIBLE', 'INELIGIBLE_EXPERIENCED'):
            return qs.filter(eligibility_classification='INELIGIBLE_EXPERIENCED')
        else:
            # STRICT REQUIREMENT: Only jobs explicitly compatible with 0-1 year
            return qs.filter(eligibility_classification='ELIGIBLE_FRESHER')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return JobDetailSerializer
        return JobSerializer

    @action(detail=False, methods=['get'])
    def meta_options(self, request):
        """Returns distinct cities, roles, and categories for dynamic UI filters."""
        cities = (
            Job.objects.filter(is_available=True)
            .values_list('city', flat=True)
            .distinct()
            .order_by('city')
        )
        work_modes = ['ONSITE', 'HYBRID', 'REMOTE']
        eligibility_categories = [
            {'value': 'FRESHER_0', 'label': 'Fresher / 0 years'},
            {'value': '0_6_MONTHS', 'label': '0–6 months'},
            {'value': '6_12_MONTHS', 'label': '6–12 months'},
            {'value': '0_1_YEAR', 'label': '0–1 year'},
            {'value': 'GRADUATE_TRAINEE', 'label': 'Graduate Trainee'},
            {'value': 'INTERNSHIP_FRESHER', 'label': 'Fresher Internship'},
        ]
        verification_statuses = [
            {'value': 'OFFICIAL_VERIFIED', 'label': 'Official Source Verified'},
            {'value': 'TRUSTED_BOARD', 'label': 'Trusted Job-Board Listing'},
            {'value': 'NEEDS_VERIFICATION', 'label': 'Needs Verification'},
        ]
        return Response({
            'cities': [c for c in cities if c],
            'work_modes': work_modes,
            'eligibility_categories': eligibility_categories,
            'verification_statuses': verification_statuses,
        })


@api_view(['GET'])
def dashboard_stats(request):
    """
    Computes genuine live database statistics for the South India Fresher Job dashboard.
    """
    now = timezone.now()
    seven_days_ago = now - timedelta(days=7)
    twenty_four_hours_ago = now - timedelta(hours=24)

    total_eligible = Job.objects.filter(
        eligibility_classification='ELIGIBLE_FRESHER',
        is_available=True
    ).count()

    official_verified = Job.objects.filter(
        eligibility_classification='ELIGIBLE_FRESHER',
        verification_status='OFFICIAL_VERIFIED',
        is_available=True
    ).count()

    trusted_board = Job.objects.filter(
        eligibility_classification='ELIGIBLE_FRESHER',
        verification_status='TRUSTED_BOARD',
        is_available=True
    ).count()

    new_discovered_7d = Job.objects.filter(
        eligibility_classification='ELIGIBLE_FRESHER',
        first_discovered_at__gte=seven_days_ago,
        is_available=True
    ).count()

    new_discovered_24h = Job.objects.filter(
        eligibility_classification='ELIGIBLE_FRESHER',
        first_discovered_at__gte=twenty_four_hours_ago,
        is_available=True
    ).count()

    unclear_count = Job.objects.filter(
        eligibility_classification='ELIGIBILITY_UNCLEAR',
        is_available=True
    ).count()

    ineligible_count = Job.objects.filter(
        eligibility_classification='INELIGIBLE_EXPERIENCED'
    ).count()

    # City breakdown for eligible jobs
    jobs_by_city = list(
        Job.objects.filter(
            eligibility_classification='ELIGIBLE_FRESHER',
            is_available=True
        )
        .values('city')
        .annotate(count=Count('id'))
        .order_by('-count')[:8]
    )

    # Experience category breakdown
    experience_breakdown = list(
        Job.objects.filter(
            eligibility_classification='ELIGIBLE_FRESHER',
            is_available=True
        )
        .values('eligibility_category')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Latest discovery run
    latest_run = DiscoveryRun.objects.order_by('-started_at').first()
    latest_run_data = None
    if latest_run:
        latest_run_data = {
            'run_id': str(latest_run.run_id),
            'status': latest_run.status,
            'started_at': latest_run.started_at,
            'completed_at': latest_run.completed_at,
            'duration_seconds': latest_run.duration_seconds,
            'jobs_discovered': latest_run.jobs_discovered,
            'duplicates_skipped': latest_run.duplicates_skipped,
            'ineligible_excluded': latest_run.ineligible_excluded,
            'sources_checked': latest_run.sources_checked,
            'sources_failed': latest_run.sources_failed,
        }

    # Top recently added eligible jobs
    recent_jobs = Job.objects.filter(
        eligibility_classification='ELIGIBLE_FRESHER',
        is_available=True
    ).select_related('source').order_by('-first_discovered_at')[:6]

    recent_jobs_serializer = JobSerializer(recent_jobs, many=True)

    return Response({
        'total_eligible_jobs': total_eligible,
        'official_verified_jobs': official_verified,
        'trusted_board_jobs': trusted_board,
        'new_discovered_7d': new_discovered_7d,
        'new_discovered_24h': new_discovered_24h,
        'unclear_experience_jobs': unclear_count,
        'ineligible_experienced_jobs': ineligible_count,
        'jobs_by_city': jobs_by_city,
        'experience_breakdown': experience_breakdown,
        'latest_run': latest_run_data,
        'recent_jobs': recent_jobs_serializer.data,
    })


@api_view(['GET'])
def health_check(request):
    """Production health check endpoint verifying database connectivity."""
    db_ok = True
    db_error = None
    try:
        Job.objects.count()
    except Exception as e:
        db_ok = False
        db_error = str(e)

    status_code = status.HTTP_200_OK if db_ok else status.HTTP_503_SERVICE_UNAVAILABLE
    return Response({
        'status': 'healthy' if db_ok else 'unhealthy',
        'application': 'South India Fresher Job Intelligence Agent',
        'version': '1.0.0',
        'database': 'connected' if db_ok else 'error',
        'error': db_error,
        'timestamp': timezone.now().isoformat(),
    }, status=status_code)
