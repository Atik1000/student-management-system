# Generated by Django 4.2.13 on 2024-08-27 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_remove_teachersubjectchoice_batch'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='credit_access',
            field=models.IntegerField(blank=True, max_length=5, null=True),
        ),
    ]
