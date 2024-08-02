# Generated by Django 4.2.13 on 2024-08-02 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_remove_teacher_staff'),
        ('app', '0013_student_semester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='course.semester'),
        ),
        migrations.AlterField(
            model_name='student',
            name='session_year_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.session_year'),
        ),
    ]
