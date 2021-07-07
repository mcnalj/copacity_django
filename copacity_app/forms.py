from django.contrib.auth.models import User
from django import forms

from .models import CheckIn
from .models import Circle
from .models import CircleMembership

class CheckInForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CheckInForm, self).__init__(*args, **kwargs)
        results = CircleMembership.objects.filter(user=self.user)
        #visibility = forms.ModelMultipleChoiceField(queryset=Circle.objects.filter(members__id=self.user.id), widget=forms.CheckboxSelectMultiple)
        # circles = []

       #self.fields['visibilty'] = forms.ModelMultipleChoiceField(queryset=Circle.objects.filter(members__id=self.user.id), widget=forms.CheckboxSelectMultiple, required=False)
        self.fields['visibilty'] = forms.ModelMultipleChoiceField(queryset=results, widget=forms.CheckboxSelectMultiple, required=False)
        # for result in results:
        #     circle = (result.circle.id, result.circle.name)
        #     circles.append(circle)
        # #self.fields['visibility'].widget.choices=circles

    class Meta:
        model = CheckIn

        fields = ['hardToday', 'goodToday', 'excitedToday', 'thoughts', 'thoughtsExplained', 'actions', 'actionsExplained', 'moodRange', 'pintaRange', 'urgency', 'visibility']
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
                    'visibility': forms.CheckboxSelectMultiple(attrs={'class': 'form-check_input'}),
        }

class CreateCircleForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CreateCircleForm, self).__init__(*args, **kwargs)
        self.fields['members'] = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Circle
        fields = ['name', 'members']
        widgets = {
                    'name':forms.TextInput(attrs={'class': 'col-sm-8 form-control'}),
                    'members': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

class ManageCirclesForm(forms.Form):
    """This is the structure that allows me to pass a value in the init."""
    """Basically, we create the field with nonsense options then override it in the init."""
    """I imagine I could also get the choices in the view, then pass choices instead of user.id. (not tested)"""
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ManageCirclesForm, self).__init__(*args, **kwargs)
        results = Circle.objects.filter(adminId=user.id).values('id', 'name')
        self.choices = []
        for result in results:
            self.choices.append((result['id'], result['name']))
        self.fields['circlesToAdmin'] = forms.ChoiceField(choices=self.choices)

    circlesToAdmin = forms.ChoiceField(choices=[])

# Are we using this?
class EditCircleForm(forms.Form):
    def __init__(self, circleId, *args, **kwargs):
        self.circleId = circleId
        super(EditCircleForm, self).__init__(*args, **kwargs)

        userResults = User.objects.all().values('id', 'username')
        self.choices = []
        for userResult in userResults:
            self.choices.append((userResult['id'], userResult['username']))

        presentCircle = Circle.objects.get(id=circleId)
        presentMembers = presentCircle.members.all().values('id', 'username')
        current = []
        for member in presentMembers:
            current.append(member['id'])
            current.append(member['username'])

        # get the members of this circle and use that to set initial
        self.fields['members'] = forms.ChoiceField(widget=forms.CheckboxSelectMultiple, choices=self.choices)
        self.fields['members'].initial=current
        self.fields['id'].initial=circleId

    id = forms.IntegerField()
    name = forms.CharField(initial='monopoly')
    createdBy = forms.CharField(initial='mcnalj')
    members = forms.ChoiceField(widget=forms.CheckboxSelectMultiple, choices={})


class UpdateCircleForm(forms.Form):
    """This is a view to practice updating circles without a model form."""
    def __init__(self, circleId, *args, **kwargs):
        self.circleId = circleId
        super(UpdateCircleForm, self).__init__(*args, **kwargs)
        circle = Circle.objects.get(id=self.circleId)
        print(circle)
        print(circle.id)
        self.fields['id'].initial=self.circleId
        self.fields['name'].initial=circle.name
        self.fields['adminId'].initial=circle.adminId
        self.fields['createdBy'].initial=circle.createdBy
        self.fields['createdOn'].initial=circle.createdOn
        self.fields['members'].initial=circle.members.all()

    id = forms.CharField(label="Circle Id", widget=forms.TextInput(attrs={'class': 'col-sm-8 form-control', 'readonly': 'true'}))
    name = forms.CharField(label="Circle Name", widget=forms.TextInput(attrs={'class': 'col-sm-8 form-control', 'placeholder':'type here'}))
    adminId = forms.CharField(label="Circle Id", widget=forms.TextInput(attrs={'class': 'col-sm-8 form-control', 'readonly': 'true'}))
    createdBy = forms.CharField(label="Creator", widget=forms.TextInput(attrs={'class': 'col-sm-8 form-control'}))
    createdOn = forms.DateTimeField(label="Created On:", widget=forms.DateTimeInput(attrs={'class': 'col-sm-8 form-control', 'readonly': 'true'}))
    members = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}), required=False)


class UpdateCircleSave(forms.Form):
    """This is a view to practice update circles without a model form."""
    id = forms.CharField(label="Circle Id", required=False, widget=forms.TextInput(attrs={'class': 'col-sm-8 form-control', 'readonly': 'true'}))
    name = forms.CharField(label="Circle Name", widget=forms.TextInput(attrs={'class': 'col-sm-8 form-control', 'placeholder':'type here'}))
    adminId = forms.CharField(label="Circle Id", required=False, widget=forms.TextInput(attrs={'class': 'col-sm-8 form-control', 'readonly': 'true'}))
    createdBy = forms.CharField(label="Creator", widget=forms.TextInput(attrs={'class': 'col-sm-8 form-control', 'required': 'False'}))
    createdOn = forms.DateTimeField(label="Created On:", required=False, widget=forms.DateTimeInput(attrs={'class': 'col-sm-8 form-control', 'readonly': 'true'}))
    members = forms.members = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}), required=False)



# I Do not think we are using anything below here. But I'm not sure about that.
# The problem is here. In saveEdittedcircles in the view we instantiate this form and it's not valid when we chack is_valid
# It would be nice to use editCircleForm because we know that data matches that but we do not have circleId
# Can we do a better job of making this form match the data?
# Also maybe we start with correct initializations of edit circle. Right now they are fake.
class SaveCircleForm(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField(initial='monopoly')
    createdBy = forms.CharField(initial='mcnalj')
    members = forms.ChoiceField(widget=forms.CheckboxSelectMultiple, choices={(1, 'mcnalj'),(2, 'Leah'), (3, 'Raizel')}, required=False)

class UpdateCircleFormDepracated(forms.ModelForm):
    """This is a view to pracice updating circles."""
    def __init__(self, circleId, *args, **kwargs):
        self.circleId = circleId
        super(UpdateCircleForm, self).__init__(*args, **kwargs)
        circle = Circle.objects.get(id=self.circleId)
        print(circle)
        print(circle.id)
        self.fields['name'].initial=circle.name
        self.fields['createdBy'].initial=circle.createdBy
#        self.fields["id"].initial=self.circleId
#        self.fields["createdOn"].initial=circle.createdOn

    class Meta:
        model = Circle

        fields = ['name', 'createdBy']

        widgets = {
#            "id": forms.TextInput(attrs={'class': 'col-sm-8 form-control', 'readonly': 'true'}),
            "name": forms.TextInput(attrs={'class': 'col-sm-8 form-control', 'placeholder':'type here'}),
#            "adminId": forms.TextInput(attrs={'class': 'col-sm-8 form-control'}),
            "createdBy": forms.TextInput(attrs={'class': 'col-sm-8 form-control'}),
        }
#    id = forms.CharField(label="Circle Id", widget=forms.TextInput(attrs={'class': 'col-sm-8 form-control', 'readonly': 'true'}))
#    name = forms.CharField(label="Circle Name", widget=forms.TextInput(attrs={'class': 'col-sm-8 form-control', 'placeholder':'type here'}))
#    createdBy = forms.CharField(label="Creator", widget=forms.TextInput(attrs={'class': 'col-sm-8 form-control'}))
#    createdOn = forms.DateTimeField(label="Created On:", widget=forms.DateTimeInput(attrs={'class': 'col-sm-8 form-control', 'readonly': 'true'}))
#    createdBy.widget(attrs={'class': 'col-sm-8 form-control'}),


class OldCheckInForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CheckInForm, self).__init__(*args, **kwargs)
        results = CircleMembership.objects.filter(user=self.user)
        circles = []
        for result in results:
            circle = (result.circle.id, result.circle.name)
            circles.append(circle)
        self.fields['visibility'].widget.choices=circles

    class Meta:
        model = CheckIn

        fields = ['hardToday', 'goodToday', 'excitedToday', 'thoughts', 'thoughtsExplained', 'actions', 'actionsExplained', 'moodRange', 'pintaRange', 'urgency', 'visibility']
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
                    'visibility': forms.Select(attrs={'class': 'form-select'}),
        }
