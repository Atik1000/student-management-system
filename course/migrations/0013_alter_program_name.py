# Generated by Django 4.2.13 on 2024-08-24 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0012_alter_semester_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
