from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from job_sources.models import JobSource
from jobs.models import Job, VerificationRecord

class JobFilterAndApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.source = JobSource.objects.create(
            name='Test Technopark Source',
            code='test_tp',
            source_type='OFFICIAL_PORTAL',
            base_url='https://technopark.in',
            trust_rating=5
        )

        # 1. Eligible fresher job (0-1 year)
        self.job_fresher = Job.objects.create(
            job_uid='uid-fresher-01',
            source=self.source,
            title='Junior Python Developer',
            company_name='UST Kerala',
            location='Technopark, Thiruvananthapuram',
            city='Thiruvananthapuram',
            state='Kerala',
            work_mode='ONSITE',
            employment_type='FULL_TIME',
            experience_min_months=0,
            experience_max_months=12,
            experience_raw_text='0-1 year',
            eligibility_category='0_1_YEAR',
            eligibility_classification='ELIGIBLE_FRESHER',
            eligibility_reason='Explicit 0-1 year experience.',
            required_skills=['Python', 'Django', 'PostgreSQL'],
            original_description='Junior Python opening in Technopark for freshers.',
            original_url='https://technopark.in/job-search',
            verification_status='OFFICIAL_VERIFIED',
            is_available=True,
            ranking_score=85.0
        )

        # 2. Ineligible experienced job (>1 year)
        self.job_senior = Job.objects.create(
            job_uid='uid-senior-02',
            source=self.source,
            title='Senior Django Architect',
            company_name='Enterprise Corp',
            location='Kochi',
            city='Kochi',
            state='Kerala',
            work_mode='HYBRID',
            employment_type='FULL_TIME',
            experience_min_months=36,
            experience_max_months=60,
            experience_raw_text='3-5 years',
            eligibility_category='EXPERIENCED_OVER_1_YEAR',
            eligibility_classification='INELIGIBLE_EXPERIENCED',
            eligibility_reason='Requires >1 year experience.',
            required_skills=['Python', 'Django', 'Microservices'],
            original_description='Mandatory 3+ years required.',
            original_url='https://infopark.in/jobs',
            verification_status='OFFICIAL_VERIFIED',
            is_available=True,
            ranking_score=0.0
        )

        # 3. Eligibility unclear job (missing experience details)
        self.job_unclear = Job.objects.create(
            job_uid='uid-unclear-03',
            source=self.source,
            title='Python Script Engineer',
            company_name='Startup XYZ',
            location='Kochi',
            city='Kochi',
            state='Kerala',
            work_mode='REMOTE',
            employment_type='CONTRACT',
            experience_min_months=0,
            experience_max_months=12,
            experience_raw_text='',
            eligibility_category='UNCLEAR',
            eligibility_classification='ELIGIBILITY_UNCLEAR',
            eligibility_reason='Experience not specified.',
            required_skills=['Python'],
            original_description='Work on Python scripts. Experience not specified.',
            original_url='https://example.com',
            verification_status='NEEDS_VERIFICATION',
            is_available=True,
            ranking_score=10.0
        )

    def test_default_api_strictly_returns_only_eligible_freshers(self):
        """Verify main job list excludes >1 year and unclear experience by default."""
        url = reverse('job-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        returned_uids = [j['job_uid'] for j in results]

        self.assertIn('uid-fresher-01', returned_uids)
        self.assertNotIn('uid-senior-02', returned_uids, "Experienced jobs must NOT appear in default results!")
        self.assertNotIn('uid-unclear-03', returned_uids, "Unclear experience jobs must NOT appear in default results!")

    def test_filter_by_unclear_eligibility(self):
        """User can explicitly query eligibility=unclear to inspect separated jobs."""
        url = reverse('job-list')
        response = self.client.get(url, {'eligibility': 'unclear'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get('results', response.data)
        returned_uids = [j['job_uid'] for j in results]
        self.assertIn('uid-unclear-03', returned_uids)
        self.assertNotIn('uid-fresher-01', returned_uids)

    def test_dashboard_stats_endpoint(self):
        """Dashboard stats must correctly reflect live counts from DB."""
        url = reverse('dashboard-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['total_eligible_jobs'], 1)
        self.assertEqual(data['ineligible_experienced_jobs'], 1)
        self.assertEqual(data['unclear_experience_jobs'], 1)
        self.assertEqual(data['official_verified_jobs'], 1)

    def test_health_check_endpoint(self):
        """Health check returns healthy status."""
        url = reverse('health-check')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'healthy')
