from django import forms
from .models import Player


class PlayerForm(forms.ModelForm):
   
    class Meta:
        model  = Player
        fields = [
            'name', 'age', 'position',
            'shooting', 'passing', 'stamina', 'defending','work_rate',
            'pace', 'strength', 'skills', 'technical_ability',
            'match_winner',
        ]
        widgets = {
            # Text / number inputs
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g. Marcus',
                'class': 'form-input',
            }),
            'age': forms.NumberInput(attrs={
                'placeholder': 'e.g. 24',
                'class': 'form-input',
            }),

            # Dropdowns
            'position': forms.Select(attrs={
                'class': 'form-input',
            }),
        

            # Sliders for 1-10 attributes
            'shooting': forms.NumberInput(attrs={
                'type': 'range', 'min': 1, 'max': 10, 'step': 1,
                'class': 'form-slider',
            }),
            'passing': forms.NumberInput(attrs={
                'type': 'range', 'min': 1, 'max': 10, 'step': 1,
                'class': 'form-slider',
            }),
            'stamina': forms.NumberInput(attrs={
                'type': 'range', 'min': 1, 'max': 10, 'step': 1,
                'class': 'form-slider',
            }),
            'defending': forms.NumberInput(attrs={
                'type': 'range', 'min': 1, 'max': 10, 'step': 1,
                'class': 'form-slider',
            }),
            'work_rate': forms.NumberInput(attrs={
                'type': 'range', 'min': 1, 'max': 10, 'step': 1,
                'class': 'form-slider',
            }),
            'pace': forms.NumberInput(attrs={
                'type': 'range', 'min': 1, 'max': 10, 'step': 1,
                'class': 'form-slider',
            }),
            'strength': forms.NumberInput(attrs={
                'type': 'range', 'min': 1, 'max': 10, 'step': 1,
                'class': 'form-slider',
            }),
            'skills': forms.NumberInput(attrs={
                'type': 'range', 'min': 1, 'max': 10, 'step': 1,
                'class': 'form-slider',
            }),
            'technical_ability': forms.NumberInput(attrs={
                'type': 'range', 'min': 1, 'max': 10, 'step': 1,
                'class': 'form-slider',
            }),

            # Slider for 1-5 match winner
            'match_winner': forms.NumberInput(attrs={
                'type': 'range', 'min': 1, 'max': 5, 'step': 1,
                'class': 'form-slider',
            }),
        }

        labels = {
            'work_rate':         'Work Rate',
            'technical_ability': 'Technical Ability',
            'match_winner':      'Match Winner',
        }