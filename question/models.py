from django.db import models
from django.urls import reverse
from course.models import Department, Semester, Subject


class Exam(models.Model):
    EXAM_TYPES = [
        ('Mid', 'Mid Exam'),
        ('Final', 'Final Exam'),
    ]

    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='exams')
    semester_name = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='exams')
    batch_number = models.CharField(max_length=20, null=True, blank=True)
    course_code = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='course_code_exams')
    name = models.CharField(max_length=5, choices=EXAM_TYPES, default='Mid')
    time = models.CharField(max_length=20, null=True, blank=True)
    marks = models.IntegerField(null=True, blank=True)
    
    # Define fields for each question
    q1_number = models.IntegerField(null=True, blank=True)
    q1_description = models.TextField(null=True, blank=True)
    q1_marks = models.IntegerField(null=True, blank=True)
    
    q2_number = models.IntegerField(null=True, blank=True)
    q2_description = models.TextField(null=True, blank=True)
    q2_marks = models.IntegerField(null=True, blank=True)
    
    q3_number = models.IntegerField(null=True, blank=True)
    q3_description = models.TextField(null=True, blank=True)
    q3_marks = models.IntegerField(null=True, blank=True)
    
    q4_number = models.IntegerField(null=True, blank=True)
    q4_description = models.TextField(null=True, blank=True)
    q4_marks = models.IntegerField(null=True, blank=True)
    
    q5_number = models.IntegerField(null=True, blank=True)
    q5_description = models.TextField(null=True, blank=True)
    q5_marks = models.IntegerField(null=True, blank=True)
    
    q6_number = models.IntegerField(null=True, blank=True)
    q6_description = models.TextField(null=True, blank=True)
    q6_marks = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"University: {self.university_name}, Course: {self.course_code}, Batch: {self.batch_number}"
    def get_absolute_url(self):
        return reverse('exam-detail', kwargs={'pk': self.pk})


