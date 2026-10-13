import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_session_id', models.CharField(db_index=True, default='default-user', max_length=100)),
                ('notes', models.TextField(blank=True)),
                ('saved_at', models.DateTimeField(auto_now_add=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_by_users', to='jobs.job')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='saved_jobs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-saved_at'],
                'unique_together': {('client_session_id', 'job')},
            },
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_session_id', models.CharField(db_index=True, default='default-user', max_length=100)),
                ('status', models.CharField(choices=[('INTERESTED', 'Interested'), ('TO_APPLY', 'To Apply'), ('APPLIED', 'Applied'), ('ASSESSMENT', 'Assessment Scheduled'), ('INTERVIEW', 'Interview'), ('OFFER', 'Offer Received'), ('REJECTED', 'Rejected'), ('WITHDRAWN', 'Withdrawn')], db_index=True, default='INTERESTED', max_length=25)),
                ('applied_date', models.DateField(blank=True, null=True)),
                ('resume_version', models.CharField(blank=True, max_length=100)),
                ('interview_date', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='jobs.job')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_applications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
                'unique_together': {('client_session_id', 'job')},
            },
        ),
    ]
