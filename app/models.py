from django.db import models
from django.contrib.auth.models import AbstractUser
from course.models import Department, Semester, Subject


# Create your models here.
class CustomUser(AbstractUser):
    USER = (
        (1,'HOD'),
        (2,'STAFF'),
        (3,'STUDENT'),
    )


    user_type = models.CharField(choices=USER,max_length=50,default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')






class Session_year(models.Model):
    session_start = models.CharField(max_length=100)
    session_end = models.CharField(max_length=100)

    def __str__(self):
        return self.session_start + " To " + self. session_end


class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    semester=models.ForeignKey(Semester, on_delete=models.DO_NOTHING)
    address = models.TextField()
    gender = models.CharField(max_length=100)
    session_year_id = models.ForeignKey(Session_year, on_delete=models.DO_NOTHING,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name


class Staff(models.Model):
    RANK_CHOICES = [
        ('CH', 'Chairman'),
        ('AP', 'Associate Professor'),
        ('AS', 'Assistant Professor'),
        ('LE', 'Lecturer'),
    ]

    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address = models.TextField()
    gender = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now= True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL,null=True, related_name='teachers_staff')
    rank = models.CharField(max_length=2, choices=RANK_CHOICES,null=True)


    def get_total_credits_per_day(self, day):
        routines = Routine.objects.filter(teacher=self, day=day)
        total_credits = sum(routine.subject.credit for routine in routines)
        return total_credits

    @staticmethod
    def get_available_teachers(subject, day, start_time, end_time):
        teachers = Staff.objects.filter(department=subject.semester.department).order_by('rank')
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
    
    def __str__(self):
        return self.admin.username
    



class Staff_Notification(models.Model):
    staff_id = models.ForeignKey(Staff,on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status =models.ImageField(null=True,default=0)

    def __str__(self):
        return self.staff_id.admin.first_name



class Staff_leave(models.Model):
    staff_id = models.ForeignKey(Staff,on_delete=models.CASCADE)
    date =  models.CharField(max_length=100)
    message = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.staff_id.admin.first_name + self.staff_id.admin.last_name
    





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
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='routines')
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('teacher', 'day', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.semester} - {self.subject} - {self.teacher} - {self.day} ({self.start_time} - {self.end_time})"