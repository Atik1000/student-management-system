from django import forms
from course.models import Department, Program
from .models import SeatPlan, Batch, Room

from django import forms
from .models import Room, Semester, SeatPlan
from .models import SeatPlanRoom




class SeatPlanRoomForm(forms.ModelForm):
    class Meta:
        model = SeatPlanRoom
        fields = ['name', 'batch', 'semester', 'department', 'program']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'batch': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
        }
        
class SeatPlanGenerateForm(forms.Form):
    room = forms.ModelChoiceField(queryset=Room.objects.all(), widget=forms.HiddenInput())
    program = forms.ModelChoiceField(queryset=Program.objects.all(), empty_label='Select Program', required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='Select Department', required=False)
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), empty_label='Select Semester', required=True)
    widgets = {
            'room': forms.Select(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['department'].queryset = Department.objects.none()
    #     self.fields['semester'].queryset = Semester.objects.none()

    #     if 'program' in self.data:
    #         try:
    #             program_id = int(self.data.get('program'))
    #             self.fields['department'].queryset = Department.objects.filter(program_id=program_id).order_by('dept_name')
    #         except (ValueError, TypeError):
    #             pass  # Invalid input from the client; ignore and fallback to empty queryset

    #     if 'department' in self.data:
    #         try:
    #             department_id = int(self.data.get('department'))
    #             self.fields['semester'].queryset = Semester.objects.filter(department_id=department_id).order_by('name')
    #         except (ValueError, TypeError):
    #             pass  # Invalid input from the client; ignore and fallback to empty queryset
    #     elif 'program' in self.data:
    #         try:
    #             program_id = int(self.data.get('program'))
    #             self.fields['semester'].queryset = Semester.objects.filter(department__program_id=program_id).order_by('name')
    #         except (ValueError, TypeError):
    #             pass  # Invalid input from the client; ignore and fallback to empty queryset

class SeatPlanForm(forms.ModelForm):
    class Meta:
        model = SeatPlan
        fields = ['room', 'student', 'seat_number']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'seat_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }
class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['name', 'sem_name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sem_name': forms.Select(attrs={'class': 'form-control'}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'num_seats', 'num_columns']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'num_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_columns': forms.NumberInput(attrs={'class': 'form-control'}),
        }
