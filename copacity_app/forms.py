from django import forms

from .models import CheckIn

class CheckInForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = ['hardToday', 'goodToday', 'excitedToday', 'thoughts', 'thoughtsExplained', 'actions', 'actionsExplained', 'moodRange', 'pintaRange', 'urgency']

        widgets = {
                    'hardToday': forms.TextInput(attrs={'class': 'col-sm-8 form-control'}),
                    'goodToday': forms.TextInput(attrs={'class': 'col-sm-8 form-control'}),
                    'excitedToday': forms.TextInput(attrs={'class': 'col-sm-8 form-control'}),
                    'thoughts': forms.RadioSelect(attrs={'class': 'form-check-input'}),
                    'thoughtsExplained': forms.TextInput(attrs={'class': 'col-sm-8 form-control', 'placeholder': 'optional explanation'}),
                    'actions': forms.RadioSelect(attrs={'class': 'form-check-input'}),
                    'actionsExplained': forms.TextInput(attrs={'class': 'col-sm-8 form-control', 'placeholder': 'optional explanation'}),
                    'moodRange': forms.NumberInput(attrs={'type': 'range', 'class': "col-sm-4 form-range", 'min': 1, 'max': 10, 'value': 5}),
                    'pintaRange': forms.NumberInput(attrs={'type': 'range', 'class': "col-sm-4 form-range", 'min': 1, 'max': 10, 'value': 5}),
                    'urgency': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }
