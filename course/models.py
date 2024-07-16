from django.db import models
from django.db.models import Sum
# from app.models import Staff


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

class Subject(models.Model):
    sub_code = models.CharField(max_length=10, null=True, blank=True)
    sub_name = models.CharField(max_length=100, null=True, blank=True)
    credit = models.IntegerField(null=True, blank=True)


class Semester(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='semesters')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='semesters')
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.program} - {self.name}"

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


# Teacher and routine 

class Teacher(models.Model):
    RANK_CHOICES = [
        ('CH', 'Chairman'),
        ('AP', 'Associate Professor'),
        ('AS', 'Assistant Professor'),
        ('LE', 'Lecturer'),
    ]

    # staff = models.OneToOneField(Staff, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teachers')
    rank = models.CharField(max_length=2, choices=RANK_CHOICES)

    def __str__(self):
        return f"{self.staff.user.username} ({self.get_rank_display()})"

    def get_total_credits_per_day(self, day):
        routines = Routine.objects.filter(teacher=self, day=day)
        total_credits = sum(routine.subject.credit for routine in routines)
        return total_credits

    @staticmethod
    def get_available_teachers(subject, day, start_time, end_time):
        teachers = Teacher.objects.filter(department=subject.semester.department).order_by('rank')
        available_teachers = []
        
        rank_priority = ['CH', 'AP', 'AS', 'LE']

        for rank in rank_priority:
            higher_ranks = rank_priority[:rank_priority.index(rank)]
            higher_rank_teachers = teachers.filter(rank__in=higher_ranks)
            higher_rank_routines = Routine.objects.filter(teacher__in=higher_rank_teachers)

            if higher_rank_routines.exists():
                continue

            rank_teachers = teachers.filter(rank=rank)

            for teacher in rank_teachers:
                if teacher.get_total_credits_per_day(day) + subject.credit <= 20:
                    routines = Routine.objects.filter(teacher=teacher, day=day)
                    conflict = False
                    for routine in routines:
                        if (start_time < routine.end_time and start_time >= routine.start_time) or (end_time <= routine.end_time and end_time > routine.start_time):
                            conflict = True
                            break
                    if not conflict:
                        available_teachers.append(teacher)

            if available_teachers:
                break

        return available_teachers


class Routine(models.Model):
    DAY_CHOICES = [

        ('Sun', 'Sunday'),
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
    ]

    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='routines')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='routines')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='routines')
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('teacher', 'day', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.semester} - {self.subject} - {self.teacher} - {self.day} ({self.start_time} - {self.end_time})"