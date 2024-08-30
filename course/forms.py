from django import forms
from .models import Program, Department, Semester, Subject

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
