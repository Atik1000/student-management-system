# Generated by Django 4.2.13 on 2024-09-06 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_student_roll_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routine',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='routine',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='routine',
            name='teacher',
        ),
        migrations.DeleteModel(
            name='Intake',
        ),
        migrations.DeleteModel(
            name='Routine',
        ),
    ]
