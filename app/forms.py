from django import forms
from course.models import Subject
from .models import  Staff,Routine



# class StaffForm(forms.ModelForm):
#     class Meta:
#         model = Staff
#         fields = ['profile_pic', 'first_name', 'last_name', 'email', 'username', 'password', 'address', 'department', 'rank', 'gender']
#         widgets = {
#             'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
#             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'password': forms.PasswordInput(attrs={'class': 'form-control'}),
#             'address': forms.Textarea(attrs={'class': 'form-control'}),
#             'department': forms.Select(attrs={'class': 'form-control'}),
#             'rank': forms.Select(attrs={'class': 'form-control'}),
#             'gender': forms.Select(attrs={'class': 'form-control'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['profile_pic'].label = 'Profile Picture'


from django.forms import ValidationError
from django import forms
from django.core.exceptions import ValidationError
from .models import Routine, Staff, Subject

class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['semester', 'subject', 'teacher', 'day', 'start_time', 'end_time']
        widgets = {
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'day': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        warnings = self.instance.clean()

        if warnings:
            raise forms.ValidationError(warnings)

