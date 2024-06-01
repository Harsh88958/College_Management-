# Generated by Django 4.2.7 on 2024-05-31 18:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('college_app', '0012_alter_feedbackstudent_feedback_reply'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('enrollment_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college_app.sessionyearmodel')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college_app.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college_app.subject')),
            ],
        ),
    ]
