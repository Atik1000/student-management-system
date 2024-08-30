from django.db import models
from django.db.models import Sum
from django.db.models import UniqueConstraint


# Create your models here.

"""
Program under department 
Department and Program under semi
"""

class Program(models.Model):
    
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    
class Department(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='department')
    dept_name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.dept_name}"



class SemesterType(models.Model):
    SEMESTER_TYPE_CHOICES = [
        ('BI', 'Bi-Semester'),
        ('TRI', 'Tri-Semester'),
    ]
    semester_type_name = models.CharField(max_length=3, choices=SEMESTER_TYPE_CHOICES, unique=True)

    def __str__(self):
        return self.get_semester_type_name_display()


class Semester(models.Model):
    program = models.ForeignKey('Program', on_delete=models.CASCADE, related_name='semesters')
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='semesters')
    name = models.CharField(max_length=20)
    semester_type = models.ForeignKey(SemesterType, on_delete=models.CASCADE, related_name='type_semesters')

    class Meta:
        constraints = [
            UniqueConstraint(fields=['program', 'department', 'name'], name='unique_program_department_semester')
        ]

    def __str__(self):
        return f"{self.program.name} - {self.name} ({self.semester_type.get_semester_type_name_display()})"



class Subject(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects')
    sub_code = models.CharField(max_length=10, null=True, blank=True)
    sub_name = models.CharField(max_length=100, null=True, blank=True)
    credit = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.sub_name}"

