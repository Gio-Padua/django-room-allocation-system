from django import forms
from .models import *

class ResidentsForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = ['name', 'address', 'family_size', 'priority', 'assigned']
        labels = {
            'name': 'Name',
            'address': 'Address',
            'family_size': 'Family Size',
            'priority': 'Priority',  # Capitalize for better clarity
            'assigned': 'Assigned',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control-user'}),
            'address': forms.Select(choices=ZONE_CHOICES, attrs={'class': 'form-control'}),
            'family_size': forms.NumberInput(attrs={'class': 'form-control-user'}),  # Use NumberInput for family size
            'priority': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # Use CheckboxInput for priority
            'assigned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # Use CheckboxInput for assigned
        }



class RoomForm(forms.ModelForm):
  class Meta:
    model = Room
    fields = ['name', 'building', 'capacity', 'priority']  # Include all fields from the model

    labels = {
      'name': 'Room Name',
      'building': 'Building Name',  # Clearer label
      'capacity': 'Maximum Capacity',
      'priority': 'High Priority',  # Indicate purpose of priority
    }

    widgets = {
      'name': forms.TextInput(attrs={'class': 'form-control'}),
      'building': forms.TextInput(attrs={'class': 'form-control'}),
      'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
      'priority': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    }

  def clean_capacity(self):
    # Custom validation for capacity field (same as before)
    capacity = self.cleaned_data['capacity']
    if capacity > 20:
      raise forms.ValidationError('Capacity cannot exceed 20 people.')
    return capacity
  

class AllocationForm(forms.ModelForm):
  class Meta:
    model = Allocation
    fields = ['resident', 'room']
    labels = {
       'resident': 'Resident',
       'room' : 'Room'
    }
    widgets = {
            'resident': forms.Select(choices=Resident.objects.all(), attrs={'class': 'form-control'}),
            'room': forms.Select(choices=Room.objects.all(), attrs={'class': 'form-control'}),  

        }
