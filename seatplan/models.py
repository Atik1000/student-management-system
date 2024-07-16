from django.db import models

# Create your models here.
# models.py
from django.db import models
from app.models import Student
from course.models import Semester

class Room(models.Model):
    number = models.IntegerField(unique=True)
    num_seats = models.IntegerField(default=40)
    num_columns = models.IntegerField(default=4)
    
    def __str__(self):
        return f'Room {self.number}'

class Batch(models.Model):
    name = models.CharField(max_length=100)
    sem_name =models.ForeignKey(Semester, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class SeatPlan(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, on_delete=models.DO_NOTHING)
    seat_number = models.IntegerField()
    
    class Meta:
        unique_together = ('room', 'seat_number')
        
    def __str__(self):
        return f'{self.student} in Room {self.room.number}  Seat {self.seat_number}'