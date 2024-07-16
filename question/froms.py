from django import forms
from .models import Exam

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'
        widgets = {
            'subject_name': forms.Select(attrs={'class': 'form-control'}),
            'department_name': forms.Select(attrs={'class': 'form-control'}),
            'semester_name': forms.Select(attrs={'class': 'form-control'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-control'}),
            'course_code': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.Select(attrs={'class': 'form-control'}),
            'time': forms.TextInput(attrs={'class': 'form-control'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'q1_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'q1_description': forms.Textarea(attrs={'class': 'form-control'}),
            'q1_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'q2_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'q2_description': forms.Textarea(attrs={'class': 'form-control'}),
            'q2_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'q3_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'q3_description': forms.Textarea(attrs={'class': 'form-control'}),
            'q3_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'q4_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'q4_description': forms.Textarea(attrs={'class': 'form-control'}),
            'q4_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'q5_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'q5_description': forms.Textarea(attrs={'class': 'form-control'}),
            'q5_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'q6_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'q6_description': forms.Textarea(attrs={'class': 'form-control'}),
            'q6_marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }
