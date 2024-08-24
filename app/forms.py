

from django.forms import ValidationError
from django import forms
from django.core.exceptions import ValidationError
from course.models import Semester, SemesterType
from .models import Routine, Staff, Subject, TeacherSubjectChoice
from django.db.models import Sum

from .models import TeacherSubjectChoice, Department, SemesterType, Semester, Subject, Intake


class IntakeForm(forms.ModelForm):
    class Meta:
        model = Intake
        fields = ['name', 'sem_name']


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
        fields = ['department', 'semester_type', 'semester', 'subject']  # Removed 'batch'
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'semester_type': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        self.staff = kwargs.pop('staff', None)
        super().__init__(*args, **kwargs)

        self.fields['department'].queryset = Department.objects.all()
        self.fields['semester_type'].queryset = SemesterType.objects.all()

        if 'department' in self.data and 'semester_type' in self.data:
            department_id = int(self.data.get('department'))
            semester_type_id = int(self.data.get('semester_type'))
            self.fields['semester'].queryset = Semester.objects.filter(
                department_id=department_id,
                semester_type_id=semester_type_id
            )
        elif self.instance.pk:
            self.fields['semester'].queryset = Semester.objects.filter(
                department=self.instance.department,
                semester_type=self.instance.semester_type
            )
        else:
            self.fields['semester'].queryset = Semester.objects.none()

        if 'semester' in self.data:
            semester_id = int(self.data.get('semester'))
            higher_ranks = ['CH', 'AP', 'AS', 'LE']
            higher_ranks = higher_ranks[:higher_ranks.index(self.staff.rank)]

            for rank in higher_ranks:
                higher_rank_staff = Staff.objects.filter(rank=rank)
                for staff in higher_rank_staff:
                    total_credits = TeacherSubjectChoice.objects.filter(
                        staff=staff
                    ).aggregate(total=Sum('subject__credit'))['total'] or 0

                    if total_credits <= 17:
                        raise ValidationError(
                            f"A higher-ranked teacher ({staff.rank}) has not completed over 17 credits. You cannot select a subject until they have selected at least 18 credits."
                        )

            higher_rank_subjects = TeacherSubjectChoice.objects.filter(
                semester_id=semester_id,
                staff__rank__in=higher_ranks
            ).values_list('subject_id', flat=True)

            already_selected_subjects = TeacherSubjectChoice.objects.filter(
                staff=self.staff,
                semester_id=semester_id
            ).values_list('subject_id', flat=True)

            self.fields['subject'].queryset = Subject.objects.filter(
                semester_id=semester_id
            ).exclude(
                id__in=higher_rank_subjects
            ).exclude(
                id__in=already_selected_subjects
            )
        elif self.instance.pk:
            self.fields['subject'].queryset = Subject.objects.filter(
                semester=self.instance.semester
            ).exclude(
                id__in=TeacherSubjectChoice.objects.filter(staff=self.instance.staff).values_list('subject_id', flat=True)
            )
        else:
            self.fields['subject'].queryset = Subject.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        selected_subject = cleaned_data.get('subject')

        if selected_subject:
            current_total_credits = TeacherSubjectChoice.objects.filter(
                staff=self.staff
            ).aggregate(total=Sum('subject__credit'))['total'] or 0

            new_total_credits = current_total_credits + selected_subject.credit

            if new_total_credits > 20:
                raise ValidationError(f"Total credit limit exceeded. Current total is {current_total_credits} credits. You cannot add more than 20 credits.")

        return cleaned_data
