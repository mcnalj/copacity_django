from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Response
from .models import CheckIn
from .forms import CheckInForm

def index(request):
    """The home page for copacity."""
    return render(request, 'copacity_app/index.html')

@login_required
def checkIns(request, nameId):
    """The page to view all checkIns."""
    print("name:")
    print(nameId)
    print("user:")
    print(request.user.id)
    if nameId == 0:
        if request.user.id == 1:
            results = CheckIn.objects.order_by('-dateTime')
        else:
            print("in the else")
            print(request.user)
            results = CheckIn.objects.filter(owner=request.user).order_by('-dateTime')
    else:
        if request.user.username == 'mcnalj':
            results = CheckIn.objects.filter(yourName=nameId).order_by('-dateTime')
            print("in the mcnalj else")
            print(nameId)
        else:
            results = CheckIn.objects.filter(owner=request.user).order_by('-dateTime')
    top = len(results)
    if top > 5:
        top = 5

    checkIns = []
    count = 0
    for result in results:
        count = count + 1
        if count <= top:
            checkIn = {}
            yourName = ""
            safeThoughts = 0
            safeActions = 0
            urgency = 4

            if result.yourName == 1:
                yourName = "Jake"
            elif result.yourName == 2:
                yourName = "Leah"
            elif result.yourName == 3:
                yourName = "Raizel"
            elif result.yourName == 4:
                yourName = "Oscar"

            if result.thoughts == 1:
                safeThoughts = "Yes"
            elif result.thoughts == 2:
                safeThoughts = "No"
            elif result.thoughts == 3:
                safeThoughts = "Maybe"

            if result.actions == 1:
                safeActions = "Yes"
            elif result.actions == 2:
                safeActions = "No"
            elif result.actions == 3:
                safeActions = "Maybe"

            if result.urgency == 1:
                urgency = "Call now"
            elif result.urgency == 2:
                urgency = "Text now"
            elif result.urgency == 3:
                urgency = "We can talk later"
            elif result.urgency == 4:
                urgency = "Not necessary to talk about it"
            elif result.urgency == 5:
                urgency = "I prefer not to talk about it"
            checkIn = {
                        'id': result.id,
                        'dateTime': result.dateTime,
                        'yourName': yourName,
                        'hardToday': result.hardToday,
                        'goodToday': result.goodToday,
                        'excitedToday': result.excitedToday,
                        'thoughts': safeThoughts,
                        'thoughtsExplained': result.thoughtsExplained,
                        'actions': safeActions,
                        'actionsExplained': result.actionsExplained,
                        'moodRange': result.moodRange,
                        'pintaRange': result.pintaRange,
                        'urgency': urgency
                        }
            checkIns.append(checkIn)

    context = {'checkIns': checkIns}
    return render(request, 'copacity_app/checkIns.html', context)

@login_required
def  new_checkIn(request):
    """Add a new checkIn"""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = CheckInForm()
    else:
        # POST data submitted; process data.
        form = CheckInForm(data=request.POST)
        print(form.errors)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.yourName = request.user.id
            instance.owner = request.user
            instance.save()
            return redirect('copacity_app:index')
        else:
            print("Save failed")
            print(request.user.id)

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'copacity_app/new_checkIn.html', context)
