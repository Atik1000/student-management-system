# Generated by Django 4.2.13 on 2024-08-02 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_remove_teacher_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='department',
        ),
        migrations.DeleteModel(
            name='Routine',
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
    ]
