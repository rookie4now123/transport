# Generated by Django 5.2 on 2025-06-14 12:45

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('station', '0003_station_is_active'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('route_name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('monitors', models.ManyToManyField(blank=True, limit_choices_to={'user_type': 'MONITOR'}, related_name='monitor_routes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RouteSchedule',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('day_of_week', models.CharField(choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday')], max_length=3)),
                ('time_of_day', models.CharField(choices=[('AM', 'Morning'), ('PM', 'Afternoon')], max_length=2)),
                ('arrival_time', models.TimeField()),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_entries', to='route.route')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='schedule_appearances', to='station.station')),
            ],
            options={
                'ordering': ['day_of_week', 'arrival_time'],
                'unique_together': {('route', 'station', 'day_of_week', 'time_of_day')},
            },
        ),
        migrations.AddField(
            model_name='route',
            name='stations',
            field=models.ManyToManyField(blank=True, related_name='routes', through='route.RouteSchedule', to='station.station'),
        ),
    ]
