from django import forms
from .models import Program, Department, Semester, Course, Subject

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['program', 'dept_name']
        widgets = {
            'program': forms.Select(attrs={'class': 'form-control'}),
            'dept_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['program', 'department', 'name', 'semester_type']
        widgets = {
            'program': forms.Select(attrs={'class': 'form-control', 'id': 'id_program'}),
            'department': forms.Select(attrs={'class': 'form-control', 'id': 'id_department'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'semester_type': forms.Select(attrs={'class': 'form-control', 'id': 'id_semester_type'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'semester',
            'course_code_1', 'course_name_1', 'credits_1',
            'course_code_2', 'course_name_2', 'credits_2',
            'course_code_3', 'course_name_3', 'credits_3',
            'course_code_4', 'course_name_4', 'credits_4',
            'course_code_5', 'course_name_5', 'credits_5',
            'course_code_6', 'course_name_6', 'credits_6',
        ]
        widgets = {
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'course_code_1': forms.TextInput(attrs={'class': 'form-control'}),
            'course_name_1': forms.TextInput(attrs={'class': 'form-control'}),
            'credits_1': forms.NumberInput(attrs={'class': 'form-control'}),
            'course_code_2': forms.TextInput(attrs={'class': 'form-control'}),
            'course_name_2': forms.TextInput(attrs={'class': 'form-control'}),
            'credits_2': forms.NumberInput(attrs={'class': 'form-control'}),
            'course_code_3': forms.TextInput(attrs={'class': 'form-control'}),
            'course_name_3': forms.TextInput(attrs={'class': 'form-control'}),
            'credits_3': forms.NumberInput(attrs={'class': 'form-control'}),
            'course_code_4': forms.TextInput(attrs={'class': 'form-control'}),
            'course_name_4': forms.TextInput(attrs={'class': 'form-control'}),
            'credits_4': forms.NumberInput(attrs={'class': 'form-control'}),
            'course_code_5': forms.TextInput(attrs={'class': 'form-control'}),
            'course_name_5': forms.TextInput(attrs={'class': 'form-control'}),
            'credits_5': forms.NumberInput(attrs={'class': 'form-control'}),
            'course_code_6': forms.TextInput(attrs={'class': 'form-control'}),
            'course_name_6': forms.TextInput(attrs={'class': 'form-control'}),
            'credits_6': forms.NumberInput(attrs={'class': 'form-control'}),
        }



# class RoutineForm(forms.ModelForm):
#     class Meta:
#         model = Routine
#         fields = ['semester', 'subject', 'day', 'start_time', 'end_time']

#     def __init__(self, *args, **kwargs):
#         self.teacher = kwargs.pop('teacher', None)
#         super().__init__(*args, **kwargs)

#         if self.teacher:
#             self.fields['semester'].queryset = self.teacher.department.semesters.all()
#             self.fields['subject'].queryset = Subject.objects.all()

#     def save(self, commit=True):
#         routine = super().save(commit=False)
#         routine.teacher = self.teacher
#         if commit:
#             routine.save()
#         return routine
    
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['sub_code', 'sub_name', 'credit', 'semester']
        widgets = {
            'sub_code': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_name': forms.TextInput(attrs={'class': 'form-control'}),
            'credit': forms.NumberInput(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control', 'id': 'id_semester'}),
        }

