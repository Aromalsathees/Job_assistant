import unittest
from agent_engine.deduplication_service import DuplicateDetectionService

class TestDuplicateDetectionService(unittest.TestCase):
    def test_uid_deterministic_and_case_insensitive(self):
        job1 = {
            'company_name': '  IBS Software  ',
            'title': 'Junior Python Developer',
            'city': 'Kochi',
            'source_code': 'infopark_kerala',
            'source_job_id': 'job-101',
        }
        job2 = {
            'company_name': 'ibs software',
            'title': 'JUNIOR PYTHON DEVELOPER',
            'city': 'kochi',
            'source_code': 'infopark_kerala',
            'source_job_id': 'job-101',
        }
        uid1 = DuplicateDetectionService.generate_job_uid(job1)
        uid2 = DuplicateDetectionService.generate_job_uid(job2)
        self.assertEqual(uid1, uid2)
        self.assertEqual(len(uid1), 32)
