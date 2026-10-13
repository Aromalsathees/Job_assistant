from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='preferences')
    client_session_id = models.CharField(max_length=100, default='default-user', unique=True, db_index=True)
    
    target_roles = models.JSONField(
        default=lambda: [
            'Python Developer', 'Django Developer', 'FastAPI Developer',
            'Junior Backend Developer', 'React + Python Developer',
            'Full Stack Developer', 'Agentic AI Developer', 'Generative AI Developer',
            'LLM Application Developer', 'RAG Developer'
        ]
    )
    target_locations = models.JSONField(
        default=lambda: [
            'Ernakulam', 'Kochi', 'Kakkanad', 'Infopark',
            'Thiruvananthapuram', 'Technopark', 'Kozhikode', 'Thrissur',
            'Chennai', 'Coimbatore', 'Bengaluru', 'Remote'
        ]
    )
    preferred_skills = models.JSONField(
        default=lambda: ['Python', 'Django', 'FastAPI', 'React', 'PostgreSQL', 'LangChain', 'Docker']
    )
    preferred_work_modes = models.JSONField(
        default=lambda: ['ONSITE', 'HYBRID', 'REMOTE']
    )
    min_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    notification_email = models.EmailField(blank=True)
    daily_schedule_enabled = models.BooleanField(default=True)
    schedule_hour = models.IntegerField(default=6)
    schedule_timezone = models.CharField(max_length=50, default='Asia/Kolkata')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences for {self.client_session_id}"
