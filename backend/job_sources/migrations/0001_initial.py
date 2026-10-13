from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='JobSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('code', models.SlugField(max_length=80, unique=True)),
                ('source_type', models.CharField(choices=[('OFFICIAL_PORTAL', 'Official IT Park / Campus Portal'), ('DIRECT_EMPLOYER', 'Direct Verified Employer Page'), ('PUBLIC_API', 'Permitted Public Job-Board API'), ('COMMUNITY_FEED', 'Authorized Industry RSS Feed')], default='PUBLIC_API', max_length=30)),
                ('base_url', models.URLField(max_length=500)),
                ('is_active', models.BooleanField(default=True)),
                ('trust_rating', models.IntegerField(default=4, help_text='1 to 5 trust scale')),
                ('last_polled_at', models.DateTimeField(blank=True, null=True)),
                ('total_jobs_found', models.IntegerField(default=0)),
                ('config', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-trust_rating', 'name'],
            },
        ),
    ]
