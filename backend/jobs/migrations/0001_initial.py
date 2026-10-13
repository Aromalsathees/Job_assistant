import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('job_sources', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_uid', models.CharField(db_index=True, max_length=64, unique=True)),
                ('source_job_id', models.CharField(blank=True, db_index=True, max_length=255)),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('company_name', models.CharField(db_index=True, max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('city', models.CharField(db_index=True, max_length=100)),
                ('state', models.CharField(default='Kerala', max_length=100)),
                ('work_mode', models.CharField(choices=[('ONSITE', 'On-site'), ('HYBRID', 'Hybrid'), ('REMOTE', 'Remote')], default='ONSITE', max_length=20)),
                ('employment_type', models.CharField(choices=[('FULL_TIME', 'Full-time'), ('INTERNSHIP', 'Internship'), ('CONTRACT', 'Contract'), ('TRAINEE', 'Trainee')], default='FULL_TIME', max_length=20)),
                ('experience_min_months', models.IntegerField(default=0)),
                ('experience_max_months', models.IntegerField(default=12)),
                ('experience_raw_text', models.CharField(blank=True, max_length=255)),
                ('eligibility_category', models.CharField(choices=[('FRESHER_0', 'Fresher / 0 years'), ('0_6_MONTHS', '0–6 months'), ('6_12_MONTHS', '6–12 months'), ('0_1_YEAR', '0–1 year'), ('GRADUATE_TRAINEE', 'Graduate Trainee'), ('INTERNSHIP_FRESHER', 'Internship (Fresher Eligible)'), ('EXPERIENCED_OVER_1_YEAR', 'Experienced (> 1 Year)'), ('UNCLEAR', 'Experience Unclear')], default='0_1_YEAR', max_length=30)),
                ('eligibility_classification', models.CharField(choices=[('ELIGIBLE_FRESHER', 'Eligible Fresher (0-1 Year)'), ('ELIGIBILITY_UNCLEAR', 'Eligibility Unclear'), ('INELIGIBLE_EXPERIENCED', 'Ineligible Experienced (>1 Year)')], db_index=True, default='ELIGIBLE_FRESHER', max_length=30)),
                ('eligibility_reason', models.TextField(blank=True)),
                ('required_skills', models.JSONField(blank=True, default=list)),
                ('preferred_skills', models.JSONField(blank=True, default=list)),
                ('salary_disclosed', models.BooleanField(default=False)),
                ('salary_min', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('salary_max', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('salary_currency', models.CharField(default='INR', max_length=10)),
                ('salary_raw_text', models.CharField(blank=True, max_length=255)),
                ('original_description', models.TextField(help_text='Verbatim original job description')),
                ('ai_summary', models.TextField(blank=True, help_text='AI-generated summary (clearly separated)')),
                ('responsibilities', models.JSONField(blank=True, default=list)),
                ('qualifications', models.JSONField(blank=True, default=list)),
                ('original_url', models.URLField(max_length=1000)),
                ('official_apply_url', models.URLField(blank=True, max_length=1000)),
                ('verification_status', models.CharField(choices=[('OFFICIAL_VERIFIED', 'Official source verified'), ('TRUSTED_BOARD', 'Trusted job-board listing'), ('NEEDS_VERIFICATION', 'Needs verification'), ('EXPIRED', 'Expired or unavailable'), ('SUSPICIOUS', 'Suspicious')], db_index=True, default='NEEDS_VERIFICATION', max_length=30)),
                ('verification_notes', models.TextField(blank=True)),
                ('is_available', models.BooleanField(db_index=True, default=True)),
                ('original_posted_date', models.DateTimeField(blank=True, null=True)),
                ('first_discovered_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('last_checked_at', models.DateTimeField(auto_now=True)),
                ('ranking_score', models.FloatField(db_index=True, default=0.0)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='job_sources.jobsource')),
            ],
            options={
                'ordering': ['-ranking_score', '-first_discovered_at'],
            },
        ),
        migrations.CreateModel(
            name='VerificationRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('OFFICIAL_VERIFIED', 'Official source verified'), ('TRUSTED_BOARD', 'Trusted job-board listing'), ('NEEDS_VERIFICATION', 'Needs verification'), ('EXPIRED', 'Expired or unavailable'), ('SUSPICIOUS', 'Suspicious')], max_length=30)),
                ('evidence_type', models.CharField(choices=[('OFFICIAL_DOMAIN_MATCH', 'Official company domain match'), ('CAMPUS_PORTAL_VERIFIED', 'IT Park official listing verified'), ('JOB_BOARD_API', 'Verified public job-board API'), ('DIRECT_CAREERS_LINK', 'Direct company careers portal application link'), ('SUSPICIOUS_FEE_FLAG', 'Suspicious monetary fee request or security deposit'), ('SUSPICIOUS_COMPANY_FLAG', 'Potential company impersonation detected'), ('HTTP_404_EXPIRED', 'Listing URL not accessible / expired')], max_length=40)),
                ('evidence_details', models.TextField()),
                ('checked_at', models.DateTimeField(auto_now_add=True)),
                ('is_valid', models.BooleanField(default=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verification_records', to='jobs.job')),
            ],
            options={
                'ordering': ['-checked_at'],
            },
        ),
        migrations.CreateModel(
            name='ProvenanceSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw_payload', models.JSONField()),
                ('http_status', models.IntegerField(default=200)),
                ('fetched_at', models.DateTimeField(auto_now_add=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snapshots', to='jobs.job')),
            ],
        ),
        migrations.AddIndex(
            model_name='job',
            index=models.Index(fields=['eligibility_classification', 'is_available'], name='jobs_job_eligibi_8db162_idx'),
        ),
        migrations.AddIndex(
            model_name='job',
            index=models.Index(fields=['city', 'state'], name='jobs_job_city_53cf4d_idx'),
        ),
        migrations.AddIndex(
            model_name='job',
            index=models.Index(fields=['verification_status'], name='jobs_job_verific_1c2b5e_idx'),
        ),
        migrations.AddIndex(
            model_name='job',
            index=models.Index(fields=['company_name'], name='jobs_job_company_a0dc0d_idx'),
        ),
    ]
