import unittest
from agent_engine.verification_service import VerificationService

class TestVerificationService(unittest.TestCase):
    def setUp(self):
        self.service = VerificationService()

    def test_suspicious_fee_demand_flagged(self):
        job = {
            'title': 'Python Developer',
            'original_description': 'Selected candidates must deposit a registration fee of Rs. 2000 before receiving the offer letter.',
            'original_url': 'https://random-job-scam.xyz/apply',
            'official_apply_url': '',
            'source_type': 'COMMUNITY_FEED',
        }
        res = self.service.verify(job)
        self.assertEqual(res['verification_status'], 'SUSPICIOUS')
        self.assertFalse(res['is_available'])
        self.assertIn('registration fee', res['evidence_details'].lower())

    def test_official_campus_portal_verified(self):
        job = {
            'title': 'Junior Python Developer',
            'original_description': 'Work in Technopark campus on core backend services.',
            'original_url': 'https://www.technopark.in/job-search',
            'official_apply_url': 'https://careers.ust.com',
            'source_type': 'OFFICIAL_PORTAL',
        }
        res = self.service.verify(job)
        self.assertEqual(res['verification_status'], 'OFFICIAL_VERIFIED')
        self.assertTrue(res['is_valid'])

    def test_trusted_job_board_verified(self):
        job = {
            'title': 'Python Engineer',
            'original_description': 'Remote software development role.',
            'original_url': 'https://remotive.com/remote-jobs/12345',
            'official_apply_url': 'https://remotive.com/remote-jobs/12345',
            'source_type': 'PUBLIC_API',
        }
        res = self.service.verify(job)
        self.assertEqual(res['verification_status'], 'TRUSTED_BOARD')
