# Generated by Django 5.2 on 2025-06-19 08:24

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('route', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('student_id', models.CharField(db_index=True, max_length=50, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('grade', models.CharField(blank=True, max_length=10, null=True)),
                ('class_name', models.CharField(blank=True, max_length=10, null=True, verbose_name='Class')),
                ('is_bus_rider', models.BooleanField(default=True)),
                ('assignment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='route.routeschedule')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
