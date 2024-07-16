# Generated by Django 4.2.13 on 2024-07-16 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0012_remove_department_program_remove_semester_department_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('num_seats', models.IntegerField(default=40)),
                ('num_columns', models.IntegerField(default=4)),
            ],
        ),
        migrations.CreateModel(
            name='SeatPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.IntegerField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seatplan.room')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.student')),
            ],
            options={
                'unique_together': {('room', 'seat_number')},
            },
        ),
    ]
