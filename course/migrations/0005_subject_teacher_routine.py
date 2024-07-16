# Generated by Django 4.2.13 on 2024-07-16 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_remove_department_program_remove_semester_department_and_more'),
        ('course', '0004_alter_semester_name_course_unique_semester'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_code', models.CharField(blank=True, max_length=10, null=True)),
                ('sub_name', models.CharField(blank=True, max_length=100, null=True)),
                ('credit', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.CharField(choices=[('CH', 'Chairman'), ('AP', 'Associate Professor'), ('AS', 'Assistant Professor'), ('LE', 'Lecturer')], max_length=2)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teachers', to='course.department')),
                ('staff', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.staff')),
            ],
        ),
        migrations.CreateModel(
            name='Routine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thu', 'Thursday'), ('Fri', 'Friday')], max_length=3)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routines', to='course.semester')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routines', to='course.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routines', to='course.teacher')),
            ],
            options={
                'unique_together': {('teacher', 'day', 'start_time', 'end_time')},
            },
        ),
    ]