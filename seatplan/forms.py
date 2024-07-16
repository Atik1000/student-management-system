from django import forms
from .models import SeatPlan, Batch, Room

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
        fields = ['name','sem_name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),

            'sem_name': forms.TextInput(attrs={'class': 'form-control'}),
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
