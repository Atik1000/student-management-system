# Generated by Django 4.2.13 on 2024-07-16 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_alter_routine_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='staff',
        ),
    ]