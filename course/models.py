from django.db import models
from django.db.models import Sum
from django.db.models import UniqueConstraint


# Create your models here.

"""
Program under department 
Department and Program under semi
"""

class Program(models.Model):
    PROGRAM_CHOICES = [
        ('BSc', 'Bachelor of Science'),
        ('MSc', 'Master of Science'),
    ]
    name = models.CharField(max_length=3, choices=PROGRAM_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

    
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



class Course(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='courses')
    
    course_code_1 = models.CharField(max_length=10, null=True, blank=True)
    course_name_1 = models.CharField(max_length=100, null=True, blank=True)
    credits_1 = models.IntegerField(null=True, blank=True)
    
    course_code_2 = models.CharField(max_length=10, null=True, blank=True)
    course_name_2 = models.CharField(max_length=100, null=True, blank=True)
    credits_2 = models.IntegerField(null=True, blank=True)
    
    course_code_3 = models.CharField(max_length=10, null=True, blank=True)
    course_name_3 = models.CharField(max_length=100, null=True, blank=True)
    credits_3 = models.IntegerField(null=True, blank=True)
    
    course_code_4 = models.CharField(max_length=10, null=True, blank=True)
    course_name_4 = models.CharField(max_length=100, null=True, blank=True)
    credits_4 = models.IntegerField(null=True, blank=True)
    
    course_code_5 = models.CharField(max_length=10, null=True, blank=True)
    course_name_5 = models.CharField(max_length=100, null=True, blank=True)
    credits_5 = models.IntegerField(null=True, blank=True)
    
    course_code_6 = models.CharField(max_length=10, null=True, blank=True)
    course_name_6 = models.CharField(max_length=100, null=True, blank=True)
    credits_6 = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.course_code_1} - {self.course_name_1} ({self.credits_1} credits)"

    def total_credits(self):
        total = sum(
            getattr(self, f'credits_{i}', 0) or 0
            for i in range(1, 7)
        )
        return total

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['semester'], name='unique_semester')
        ]
