# Generated by Django 4.2.13 on 2024-08-07 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_remove_student_session_year_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='password',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='username',
        ),
    ]
