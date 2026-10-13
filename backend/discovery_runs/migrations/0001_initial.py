import uuid
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='DiscoveryRun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('RUNNING', 'Running'), ('SUCCESS', 'Success'), ('PARTIAL_SUCCESS', 'Partial Success'), ('FAILED', 'Failed')], db_index=True, default='PENDING', max_length=20)),
                ('started_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('duration_seconds', models.FloatField(default=0.0)),
                ('sources_checked', models.JSONField(blank=True, default=list)),
                ('sources_failed', models.JSONField(blank=True, default=list)),
                ('jobs_discovered', models.IntegerField(default=0)),
                ('jobs_updated', models.IntegerField(default=0)),
                ('duplicates_skipped', models.IntegerField(default=0)),
                ('ineligible_excluded', models.IntegerField(default=0)),
                ('unclear_separated', models.IntegerField(default=0)),
                ('official_verified_count', models.IntegerField(default=0)),
                ('trusted_board_count', models.IntegerField(default=0)),
                ('summary_notes', models.TextField(blank=True)),
                ('error_message', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['-started_at'],
            },
        ),
    ]
