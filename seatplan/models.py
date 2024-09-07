from django.db import models

from app.models import Student
from course.models import Department, Program, Semester
from app.models import Student

class Room(models.Model):
    number = models.IntegerField(unique=True)
    num_seats = models.IntegerField(default=40)
    num_columns = models.IntegerField(default=4)

    def __str__(self):

        return f'Room {self.number}'
    
    @property
    def calculateSeatPercol(self):
        return int(self.num_seats/self.num_columns)



class SeatPlan(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    col_num=models.IntegerField(default=0)
    seat_number = models.IntegerField(default=0)  # E.g., "1-1", "1-2"

    def __str__(self):
        return f"{self.student} - {self.seat_number} in Room {self.room.number}"
    
                