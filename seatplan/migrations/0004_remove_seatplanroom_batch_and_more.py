# Generated by Django 4.2.13 on 2024-08-28 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_student_roll_no'),
        ('course', '0013_alter_program_name'),
        ('seatplan', '0003_seatplanroom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seatplanroom',
            name='batch',
        ),
        migrations.RemoveField(
            model_name='seatplanroom',
            name='department',
        ),
        migrations.RemoveField(
            model_name='seatplanroom',
            name='program',
        ),
        migrations.RemoveField(
            model_name='seatplanroom',
            name='room',
        ),
        migrations.RemoveField(
            model_name='seatplanroom',
            name='semester',
        ),
        migrations.AlterUniqueTogether(
            name='seatplan',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='seatplan',
            name='semester',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='course.semester'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seatplan',
            name='seat_number',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='seatplan',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.student'),
        ),
        migrations.DeleteModel(
            name='Batch',
        ),
        migrations.DeleteModel(
            name='SeatPlanRoom',
        ),
    ]
