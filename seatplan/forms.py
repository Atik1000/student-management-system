from django import forms
from .models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'num_seats', 'num_columns']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'num_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_columns': forms.NumberInput(attrs={'class': 'form-control'}),
        }
