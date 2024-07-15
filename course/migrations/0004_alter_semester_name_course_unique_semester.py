# Generated by Django 4.2.13 on 2024-07-14 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_remove_course_course_code_remove_course_course_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AddConstraint(
            model_name='course',
            constraint=models.UniqueConstraint(fields=('semester',), name='unique_semester'),
        ),
    ]
