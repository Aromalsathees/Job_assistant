from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from job_sources.models import JobSource
from jobs.models import Job
from applications.models import SavedJob, JobApplication

class ApplicationTrackerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.source = JobSource.objects.create(
            name='Test Source',
            code='test_src',
            source_type='OFFICIAL_PORTAL',
            base_url='https://example.com'
        )
        self.job = Job.objects.create(
            job_uid='uid-test-app',
            source=self.source,
            title='React + Python Developer',
            company_name='Kochi Tech',
            location='Kochi',
            city='Kochi',
            state='Kerala',
            work_mode='ONSITE',
            employment_type='FULL_TIME',
            eligibility_classification='ELIGIBLE_FRESHER',
            original_description='Build apps in React and Python.',
            original_url='https://example.com/job',
            verification_status='OFFICIAL_VERIFIED'
        )

    def test_save_and_retrieve_job(self):
        # Bookmark job
        url = reverse('savedjob-list')
        resp = self.client.post(
            url,
            {'job': self.job.id, 'notes': 'Applying this weekend'},
            HTTP_X_CLIENT_SESSION='test-session-1'
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Retrieve saved jobs
        resp_get = self.client.get(url, HTTP_X_CLIENT_SESSION='test-session-1')
        self.assertEqual(resp_get.status_code, status.HTTP_200_OK)
        results = resp_get.data.get('results', resp_get.data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['job_details']['title'], 'React + Python Developer')

    def test_application_tracker_status_updates(self):
        url = reverse('jobapplication-list')
        resp = self.client.post(
            url,
            {
                'job': self.job.id,
                'status': 'APPLIED',
                'applied_date': '2026-10-12',
                'notes': 'Applied via official portal'
            },
            HTTP_X_CLIENT_SESSION='test-session-1'
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        app_id = resp.data['id']

        # Transition to INTERVIEW
        detail_url = reverse('jobapplication-detail', args=[app_id])
        resp_update = self.client.patch(
            detail_url,
            {'status': 'INTERVIEW', 'notes': 'Interview round 1 scheduled'},
            HTTP_X_CLIENT_SESSION='test-session-1'
        )
        self.assertEqual(resp_update.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_update.data['status'], 'INTERVIEW')
