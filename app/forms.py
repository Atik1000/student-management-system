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

    def __init__(self, *args, **kwargs):
        super(RoutineForm, self).__init__(*args, **kwargs)
        if 'teacher' in self.data:
            teacher_id = self.data.get('teacher')
            try:
                teacher = Staff.objects.get(id=teacher_id)
                self.filter_subjects_based_on_rank(teacher)
            except Staff.DoesNotExist:
                pass
        elif self.instance and self.instance.pk:
            teacher = self.instance.teacher
            self.filter_subjects_based_on_rank(teacher)

    def filter_subjects_based_on_rank(self, teacher):
        if self.is_bound and self.is_valid():
            cleaned_data = self.cleaned_data
            taken_subjects = Routine.objects.filter(subject__in=self.fields['subject'].queryset)
            conflicting_routines = taken_subjects.filter(
                day=cleaned_data.get('day'),
                start_time__lt=cleaned_data.get('end_time'),
                end_time__gt=cleaned_data.get('start_time')
            )

            conflicting_subjects = []
            for routine in conflicting_routines:
                if routine.teacher.rank < teacher.rank:
                    conflicting_subjects.append(routine.subject.id)
                elif routine.teacher.rank > teacher.rank:
                    raise ValidationError(f'This subject has already been taken by {routine.teacher.rank_display()}')

            self.fields['subject'].queryset = self.fields['subject'].queryset.exclude(id__in=conflicting_subjects)

