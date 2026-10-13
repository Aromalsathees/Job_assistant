import unittest
from agent_engine.eligibility_service import EligibilityAgent

class TestStrictEligibilityAgent(unittest.TestCase):
    def setUp(self):
        self.agent = EligibilityAgent()

    def test_explicit_fresher_classified_eligible(self):
        job = {
            'title': 'Python Developer',
            'experience_raw_text': '0 years / Freshers welcome',
            'original_description': 'Fresh graduates with strong core Python skills.',
            'employment_type': 'FULL_TIME',
        }
        res = self.agent.evaluate(job)
        self.assertEqual(res['eligibility_classification'], 'ELIGIBLE_FRESHER')
        self.assertEqual(res['eligibility_category'], 'FRESHER_0')
        self.assertEqual(res['experience_max_months'], 0)

    def test_zero_to_one_year_classified_eligible(self):
        job = {
            'title': 'Django Backend Engineer',
            'experience_raw_text': '0-1 year experience',
            'original_description': 'Building REST APIs in Django.',
            'employment_type': 'FULL_TIME',
        }
        res = self.agent.evaluate(job)
        self.assertEqual(res['eligibility_classification'], 'ELIGIBLE_FRESHER')
        self.assertEqual(res['eligibility_category'], '0_1_YEAR')
        self.assertLessEqual(res['experience_max_months'], 12)

    def test_zero_to_six_months_classified_eligible(self):
        job = {
            'title': 'FastAPI Developer',
            'experience_raw_text': '0-6 months',
            'original_description': 'Asynchronous APIs in Python.',
            'employment_type': 'FULL_TIME',
        }
        res = self.agent.evaluate(job)
        self.assertEqual(res['eligibility_classification'], 'ELIGIBLE_FRESHER')
        self.assertEqual(res['eligibility_category'], '0_6_MONTHS')

    def test_graduate_trainee_classified_eligible(self):
        job = {
            'title': 'Graduate Engineer Trainee - Python',
            'experience_raw_text': 'Trainee position',
            'original_description': 'Undergo 3 months intensive training.',
            'employment_type': 'TRAINEE',
        }
        res = self.agent.evaluate(job)
        self.assertEqual(res['eligibility_classification'], 'ELIGIBLE_FRESHER')
        self.assertEqual(res['eligibility_category'], 'GRADUATE_TRAINEE')

    def test_internship_classified_eligible(self):
        job = {
            'title': 'AI Agent Intern',
            'experience_raw_text': 'Internship',
            'original_description': 'Work with LangChain and LLMs.',
            'employment_type': 'INTERNSHIP',
        }
        res = self.agent.evaluate(job)
        self.assertEqual(res['eligibility_classification'], 'ELIGIBLE_FRESHER')
        self.assertEqual(res['eligibility_category'], 'INTERNSHIP_FRESHER')

    def test_senior_or_lead_strictly_excluded(self):
        job = {
            'title': 'Senior Python Developer',
            'experience_raw_text': '0-1 year',  # Contradictory title
            'original_description': 'Lead development team.',
            'employment_type': 'FULL_TIME',
        }
        res = self.agent.evaluate(job)
        self.assertEqual(res['eligibility_classification'], 'INELIGIBLE_EXPERIENCED')

    def test_two_plus_years_strictly_excluded(self):
        job = {
            'title': 'Python Developer',
            'experience_raw_text': 'Minimum 3+ years of mandatory software development experience',
            'original_description': 'Must have at least 3 years in Django.',
            'employment_type': 'FULL_TIME',
        }
        res = self.agent.evaluate(job)
        self.assertEqual(res['eligibility_classification'], 'INELIGIBLE_EXPERIENCED')
        self.assertEqual(res['eligibility_category'], 'EXPERIENCED_OVER_1_YEAR')

    def test_junior_alone_without_experience_is_unclear(self):
        # STRICT RULE: Do not infer fresher eligibility from the word "Junior" alone!
        job = {
            'title': 'Junior Python Developer',
            'experience_raw_text': '',
            'original_description': 'Looking for an enthusiastic engineer.',
            'employment_type': 'FULL_TIME',
        }
        res = self.agent.evaluate(job)
        self.assertEqual(res['eligibility_classification'], 'ELIGIBILITY_UNCLEAR')
        self.assertEqual(res['eligibility_category'], 'UNCLEAR')

    def test_missing_experience_is_unclear(self):
        job = {
            'title': 'Software Engineer - Python',
            'experience_raw_text': '',
            'original_description': 'Great salary, nice culture, join our team.',
            'employment_type': 'FULL_TIME',
        }
        res = self.agent.evaluate(job)
        self.assertEqual(res['eligibility_classification'], 'ELIGIBILITY_UNCLEAR')
