

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


class TeacherSubjectChoiceForm(forms.ModelForm):
    class Meta:
        model = TeacherSubjectChoice
        fields = ['department', 'semester_type', 'semester', 'subject']

    def __init__(self, *args, **kwargs):
        staff = kwargs.pop('staff', None)
        super(TeacherSubjectChoiceForm, self).__init__(*args, **kwargs)

        # Initial queryset for semester types and semesters is empty
        self.fields['semester_type'].queryset = SemesterType.objects.none()
        self.fields['semester'].queryset = Semester.objects.none()
        self.fields['subject'].queryset = Subject.objects.none()

        # If editing an existing instance
        if self.instance and self.instance.pk:
            department_id = self.instance.department_id
            semester_type_id = self.instance.semester_type_id
            semester_id = self.instance.semester_id

            self.fields['semester_type'].queryset = SemesterType.objects.filter(
                type_semesters__department_id=department_id
            ).distinct()

            self.fields['semester'].queryset = Semester.objects.filter(
                semester_type_id=semester_type_id,
                department_id=department_id
            ).distinct()

            self.fields['subject'].queryset = Subject.objects.filter(
                semester_id=semester_id,
                semester_type_id=semester_type_id,
                department_id=department_id
            ).distinct()

        # Exclude subjects already selected by higher-ranked teachers
        if staff:
            higher_ranks = ['CH', 'AP', 'AS', 'LE']
            staff_rank_index = higher_ranks.index(staff.rank)
            higher_ranks = higher_ranks[:staff_rank_index]

            # Ensure you only access the semester if it exists
            if self.instance and self.instance.pk and self.instance.semester:
                selected_subjects = TeacherSubjectChoice.objects.filter(
                    semester=self.instance.semester,
                    subject__in=Subject.objects.filter(department=self.instance.department)
                ).filter(staff__rank__in=higher_ranks).values_list('subject_id', flat=True)

                self.fields['subject'].queryset = self.fields['subject'].queryset.exclude(id__in=selected_subjects)
