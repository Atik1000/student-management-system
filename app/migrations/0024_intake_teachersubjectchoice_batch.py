# Generated by Django 4.2.13 on 2024-08-21 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0012_alter_semester_name_and_more'),
        ('app', '0023_alter_routine_unique_together_teachersubjectchoice'),
    ]

    operations = [
        migrations.CreateModel(
            name='Intake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sem_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.semester')),
            ],
        ),
        migrations.AddField(
            model_name='teachersubjectchoice',
            name='batch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='subject_choices', to='app.intake'),
            preserve_default=False,
        ),
    ]