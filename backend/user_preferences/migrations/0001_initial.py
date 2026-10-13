import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_session_id', models.CharField(db_index=True, default='default-user', max_length=100, unique=True)),
                ('target_roles', models.JSONField(default=list)),
                ('target_locations', models.JSONField(default=list)),
                ('preferred_skills', models.JSONField(default=list)),
                ('preferred_work_modes', models.JSONField(default=list)),
                ('min_salary', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('notification_email', models.EmailField(blank=True, max_length=254)),
                ('daily_schedule_enabled', models.BooleanField(default=True)),
                ('schedule_hour', models.IntegerField(default=6)),
                ('schedule_timezone', models.CharField(default='Asia/Kolkata', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='preferences', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
