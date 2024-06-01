# Generated by Django 4.2.7 on 2024-05-25 18:25

import college_app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('college_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.UUIDField(default=uuid.UUID('10a512f9-cff6-4c80-979c-383bd8cf6403'), primary_key=True, serialize=False, unique=True)),
                ('course_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SessionYearModel',
            fields=[
                ('course_id', models.UUIDField(default=uuid.UUID('7067309c-685d-4740-9753-e004c1872511'), primary_key=True, serialize=False, unique=True)),
                ('session_start_year', models.DateField()),
                ('session_last_year', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.UUIDField(default=uuid.UUID('87f645eb-1e58-45b1-b1aa-4356326a9747'), primary_key=True, serialize=False, unique=True)),
                ('gender', models.CharField(max_length=50)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to=college_app.models.generate_image_path)),
                ('address', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='college_app.course')),
                ('session_year_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college_app.sessionyearmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staff_id', models.UUIDField(default=uuid.UUID('802781a7-a455-45b4-a1dd-6174d08f4a75'), primary_key=True, serialize=False, unique=True)),
                ('gender', models.CharField(max_length=50)),
                ('address', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
