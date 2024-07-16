# Generated by Django 4.2.13 on 2024-07-12 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('university_name', models.CharField(blank=True, max_length=100, null=True)),
                ('subject_name', models.CharField(blank=True, max_length=100, null=True)),
                ('department_name', models.CharField(blank=True, max_length=100, null=True)),
                ('semester_name', models.CharField(blank=True, max_length=50, null=True)),
                ('batch_number', models.CharField(blank=True, max_length=20, null=True)),
                ('course_code', models.CharField(blank=True, max_length=20, null=True)),
                ('time', models.CharField(blank=True, max_length=20, null=True)),
                ('marks', models.IntegerField(blank=True, null=True)),
                ('q1_number', models.IntegerField(blank=True, null=True)),
                ('q1_description', models.TextField(blank=True, null=True)),
                ('q1_marks', models.IntegerField(blank=True, null=True)),
                ('q2_number', models.IntegerField(blank=True, null=True)),
                ('q2_description', models.TextField(blank=True, null=True)),
                ('q2_marks', models.IntegerField(blank=True, null=True)),
                ('q3_number', models.IntegerField(blank=True, null=True)),
                ('q3_description', models.TextField(blank=True, null=True)),
                ('q3_marks', models.IntegerField(blank=True, null=True)),
                ('q4_number', models.IntegerField(blank=True, null=True)),
                ('q4_description', models.TextField(blank=True, null=True)),
                ('q4_marks', models.IntegerField(blank=True, null=True)),
                ('q5_number', models.IntegerField(blank=True, null=True)),
                ('q5_description', models.TextField(blank=True, null=True)),
                ('q5_marks', models.IntegerField(blank=True, null=True)),
                ('q6_number', models.IntegerField(blank=True, null=True)),
                ('q6_description', models.TextField(blank=True, null=True)),
                ('q6_marks', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]