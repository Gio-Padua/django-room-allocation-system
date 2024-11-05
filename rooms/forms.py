from django import forms
from .models import *

class ResidentsForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = ['lname','fname', 'address', 'street', 'family_size', 'priority_members', 'priority_category', 'priority', 'assigned']
        labels = {
            'lname': 'Last Name',
            'fname': 'First Name',
            'address': 'Address',
            'family_size': 'Family Size',
            'street': 'Street',
            'priority_members': 'Number of Priority Members',
            'priority_category': 'Category of Priority Members',
            'priority': 'Priority',  # Capitalize for better clarity
            'assigned': 'Assigned',
        }
        widgets = {
            'lname': forms.TextInput(attrs={'class': 'form-control-user'}),
            'fname': forms.TextInput(attrs={'class': 'form-control-user'}),
            'address': forms.Select(choices=ZONE_CHOICES, attrs={'class': 'form-control'}),
            'family_size': forms.NumberInput(attrs={'class': 'form-control-user'}), 
            'street': forms.TextInput(attrs={'class': 'form-control-user'}), 
            'priority_members': forms.NumberInput(attrs={'class': 'form-control-user'}),
            'priority_category': forms.Select(choices=PRIORITY_CATEGORY, attrs={'class': 'form-control'}), 
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
              'resident': forms.Select(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control'}),

        }
