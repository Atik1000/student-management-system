# Generated by Django 4.2.13 on 2024-08-18 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_remove_teacher_department_delete_routine_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SemesterType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_type_name', models.CharField(choices=[('BI', 'Bi-Semester'), ('TRI', 'Tri-Semester')], max_length=3, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='subject',
            name='semester',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='course.semester'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='semester',
            name='semester_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='type_semesters', to='course.semestertype'),
            preserve_default=False,
        ),
    ]
