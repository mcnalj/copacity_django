from django import forms

from .models import CheckIn

class CheckInForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = ['yourName', 'hardToday', 'goodToday', 'excitedToday', 'thoughts', 'thoughtsExplained', 'actions', 'actionsExplained', 'moodRange', 'pintaRange', 'urgency']
        labels = {  'hardToday': 'One thing that was hard today:',
                    'goodToday': 'One thing that was good today:',
                    'excitedToday': 'One thing I am excited about:',
                    'moodRange': 'Today I am feeling:',
                    'pintaRange': 'I need a Pinta picture:',
                }
        widgets = {
                    'yourName': forms.Select(attrs={'class':'col-sm-8 form-select'}),
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
