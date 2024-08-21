

from django.forms import ValidationError
from django import forms
from django.core.exceptions import ValidationError
from course.models import Semester, SemesterType
from .models import Routine, Staff, Subject, TeacherSubjectChoice
class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['semester', 'subject', 'day', 'start_time', 'end_time']  # Removed 'teacher'
        widgets = {
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'day': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        warnings = self.instance.clean()

        if warnings:
            raise forms.ValidationError(warnings)

        # Additional custom validation (if needed) can be added here.

        return cleaned_data



from .models import TeacherSubjectChoice, Department, SemesterType, Semester, Subject, Intake



class TeacherSubjectChoiceForm(forms.ModelForm):
    class Meta:
        model = TeacherSubjectChoice
        fields = ['department', 'semester_type', 'semester', 'batch', 'subject']

    def __init__(self, *args, **kwargs):
        staff = kwargs.pop('staff', None)
        super().__init__(*args, **kwargs)

        # Initially show all departments and semester types
        self.fields['department'].queryset = Department.objects.all()
        self.fields['semester_type'].queryset = SemesterType.objects.all()

        # Filter semesters based on department and semester type
        if 'department' in self.data and 'semester_type' in self.data:
            department_id = int(self.data.get('department'))
            semester_type_id = int(self.data.get('semester_type'))
            self.fields['semester'].queryset = Semester.objects.filter(
                department_id=department_id, 
                semester_type_id=semester_type_id
            )
        elif self.instance.pk:  # Handle editing of existing instances
            self.fields['semester'].queryset = Semester.objects.filter(
                department=self.instance.department,
                semester_type=self.instance.semester_type
            )
        else:
            self.fields['semester'].queryset = Semester.objects.none()

        # Filter batch and subjects based on the selected semester
        if 'semester' in self.data:
            semester_id = int(self.data.get('semester'))
            self.fields['batch'].queryset = Intake.objects.filter(sem_name_id=semester_id)  # Use sem_name_id
            self.fields['subject'].queryset = Subject.objects.filter(semester_id=semester_id)
        elif self.instance.pk:
            # Handle case where editing an instance
            self.fields['batch'].queryset = Intake.objects.filter(sem_name=self.instance.semester)
            self.fields['subject'].queryset = Subject.objects.filter(semester=self.instance.semester)
        else:
            self.fields['batch'].queryset = Intake.objects.none()
            self.fields['subject'].queryset = Subject.objects.none()
