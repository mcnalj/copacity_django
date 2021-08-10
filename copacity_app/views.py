from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.views import PasswordChangeDoneView

from django.contrib.auth.models import User
from .models import Response
from .models import CheckIn
from .models import Circle
from .models import CircleMembership
from .forms import CheckInForm
from .forms import CreateCircleForm
from .forms import ManageCirclesForm
from .forms import EditCircleForm
from .forms import SaveCircleForm
from .forms import UpdateCircleForm
from .forms import CheckInRequestForm
from .forms import CheckInSendRequestForm

from twilio.rest import Client

from .credentials import Credentials

import datetime

def index(request):
    """The home page for copacity."""
    return render(request, 'copacity_app/index.html')

@login_required
def new_checkIn(request):
    """Add a new checkIn"""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = CheckInForm(request.user)
    else:
        # POST data submitted; process data.
        form = CheckInForm(request.user, data=request.POST)
        if form.is_valid():
            circles = form.cleaned_data['visibility']
            instance = form.save(commit=False)
            instance.yourName = request.user.id
            instance.owner = request.user
            instance.save()
            #instance.visibility.add(firstCircle)
            instance.visibility.set(circles)
            return redirect('copacity_app:index')
        else:
            print("Save failed")
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'copacity_app/new_checkIn.html', context)

@login_required
def yourCheckIns(request):
    """The page to view all of your checkIns."""
    circles = []
    circles = CheckIn.objects.filter(owner=request.user).order_by('-dateTime')

    context = {'circles': circles}
    return render(request, 'copacity_app/your_checkins.html', context)

@login_required
def yourCircles(request):
    """The page for yourCircles that allows you to pick a circle to view check-ins or details."""
    results = CircleMembership.objects.filter(user=request.user)
    circles = []
    for result in results:
        members = result.circle.members.all()
        people = []
        for member in members:
            people.append(member.username)
        circle = {
            'circleId': result.circle.id,
            'name': result.circle.name,
            'adminId': result.circle.adminId,
            'createdBy': result.circle.createdBy,
            'createdOn': result.circle.createdOn,
            'people': people
        }
        circles.append(circle)

    context = {'circles': circles}
    return render(request, 'copacity_app/your_circles_checkins.html', context)

@login_required
def circles_checkins_view(request, circleId):
    """Check-ins that have visibility for the passed circleId."""
    circle = Circle.objects.get(id=circleId)
    circleName = circle.name
    checkIns = circle.visibility.all()
    for checkIn in checkIns:
        checkIn.yourName = User.objects.get(id=checkIn.yourName)

    context = {'checkIns': checkIns, 'circleName': circleName}
    return render (request, 'copacity_app/circles_checkins_view.html', context)

@login_required
def circle_details(request, circleId):
    """Details for the passed circleId."""
    circle = Circle.objects.get(id=circleId)
    members = circle.members.all()
    people = []
    for member in members:
        people.append(member.username)

    context = {'circle': circle, 'people': people}
    return render (request, 'copacity_app/circle_details.html', context)

@login_required
def createCircle(request):
    """Page to create a circle and associate members."""
    if request.method != 'POST':
        form = CreateCircleForm(request.user)
    else:
        form = CreateCircleForm(request.user, data=request.POST)
        if form.is_valid():
            members = form.cleaned_data['members']
            instance = form.save(commit=False)
            instance.adminId = request.user
            instance.createdBy = request.user.id
            ts = datetime.datetime.now()
            instance.createdOn = ts
            instance.save()
            instance.members.set(members, through_defaults={'inviter': request.user})
            return redirect('copacity_app:index')
        else:
            print("Save create circle failed!")

    context = {'form': form}
    return render(request, 'copacity_app/create_circle.html', context)

@login_required
def manage_circles(request):
    """List the circles you belong to in dropdown. Buttons for view checkins or edit circle."""
    if request.method != 'POST':
        form = ManageCirclesForm(request.user)
    else:
        form = ManageCirclesForm(request.user, data=request.POST)
        if form.is_valid():
            circleId = form.cleaned_data['circlesToAdmin']
            circleObj = Circle.objects.get(id=circleId)
            form = UpdateCircleForm(circleId)
            circleInstance = Circle.objects.get(id=circleId)
            context = {'form':form, 'circleInstance':circleInstance}
            return render(request, 'copacity_app/update_circle.html', context)
        else:
            print("There were errors!")

    context = {'form': form}
    return render(request, 'copacity_app/manage_circles.html', context)


@login_required
def circles_checkins(request):
    if request.method != 'POST':
        return redirect('copacity_app:index')
    else:
        form = ManageCirclesForm(request.user, data=request.POST)
        form.is_valid()
        circleName = Circle.objects.filter(id=form.cleaned_data['circlesToAdmin']).values('name')
        circles = CheckIn.objects.filter(id=form.cleaned_data['circlesToAdmin']).order_by('-dateTime')

        context = {'circles': circles, 'circleName':circleName[0]['name']}
        return render(request, 'copacity_app/checkins_admin_view.html', context)


@login_required
def update_circle(request):
    """Update a circle and saving to the DB."""
    if request.method != 'POST':
        form = ManageCirclesForm(request.user, data=request.POST)
        if form.is_valid():
            circleId = form.cleaned_data['circlesToAdmin']
            circleObj = Circle.objects.get(id=circleId)
        form = UpdateCircleForm(circleId)
        circleInstance = Circle.objects.get(id=circleId)
    else:
        form = UpdateCircleSave(data=request.POST)
        if form.is_valid():
            members = form.cleaned_data['members']
            circle = Circle.objects.get(id=form.cleaned_data['id'])
            circle.name = form.cleaned_data["name"]
            circle.createdBy= form.cleaned_data["createdBy"]
            instance = circle.save()
            circle.members.set(members, through_defaults={'inviter': request.user})
            circleInstance = instance
        else:
            return redirect('copacity_app:index')

    context = {'form':form, 'circleInstance':circleInstance}
    return render(request, 'copacity_app/update_circle.html', context)


@login_required
def request_checkin(request):
    """Page to send an SMS to request a checkin."""
    if request.method != 'POST':
        print("Requesting GET check-in!")
    else:
        print("Requesting POST check-in!")
        form = ManageCirclesForm(request.user, data=request.POST)
        print(form) # for some reason if we don't have this, form has no cleaned_data?
        if form.is_valid:
            circleId = form.cleaned_data['circlesToAdmin']
            form = CheckInRequestForm(circleId)
            context = {'form':form}
            return render(request, 'copacity_app/request_checkin.html', context)
        else:
            print("Invalid form, need error handling.")
    return redirect('copacity_app:index')

@login_required
def send_checkin_request(request):
    if request.method != 'POST':
        print("We have and error.")
    else:
        print("In the send post . .. .")
        account_sid = Credentials.account_sid
        auth_token = Credentials.auth_token
        form = CheckInSendRequestForm(data=request.POST)
        if form.is_valid():
            circle_name = form.cleaned_data["circle_name"]
            member_name = form.cleaned_data["name"]
            phoneNumber = form.cleaned_data["phoneNumber"]
            phoneNumber = '+1' + str(phoneNumber)
            print(phoneNumber)
            client = Client(account_sid, auth_token)
            content = "Hi " + member_name + ", " + request.user.username + " wants you to check in to " + circle_name + " at https://co-pacity.herokuapp.com/."
            print(content)
            message = client.messages.create(
                from_='+12056354461',
                body = content,
                to = phoneNumber
            )
            print("Request Sent!")
        else:
            print("Form not valid")
            print(form.errors)
    return redirect('copacity_app:index')





# Are we using this?
@login_required
def edit_circles(request):
    """Add or remove members from a circle."""
    if request.method != 'POST':
        print("Wow! Edit circles works!")
        return redirect('copacity_app:index')
    else:
        form = ManageCirclesForm(request.user, data=request.POST)
        if form.is_valid():
            circleId = form.cleaned_data['circlesToAdmin']
            circleObj = Circle.objects.get(id=circleId)
        form = EditCircleForm(circleId)
        context = {'form':form}
        return render(request, 'copacity_app/edit_circles.html', context)

# Are we using this?
# This doesn't seem to be updating the database.
@login_required
def save_editted_circles(request):
    """To update the database with editted circles."""
    print(request.method)
    if request.method != 'POST':
        print("Wow! Save editted circles works!")
        return redirect('copacity_app:index')

    else:
        form = SaveCircleForm(data=request.POST)
        print("This is the form after SaveCircleForm")
        print(form)
        if form.is_valid():
            circle = Circle.objects.get(id=form.cleaned_data['id'])
            print("Here is circle.")
            print(circle)
            circle.name = form.cleaned_data['name']
            circle.createdBy = form.cleaned_data['createdBy']
            circle.save(update_fields=['name', 'createdBy'])
            for member in form.cleaned_data['members']:
                circle.members.add(member)
            print(form.errors)
        else:
            print(form.errors)

        context = {'form':form}
        return redirect('copacity_app:index')

# We are not using this.
@login_required
def add_mtm(request):
    """ This is a view to test SQL."""
    # ts = datetime.datetime.now()
    # circle = Circle.objects.create(name='tester2', adminId=request.user, createdBy='mcnalj', createdOn=ts)
    # circle.members.add(request.user, through_defaults={'inviter': request.user})
    #
    # results = Circle.objects.filter(name='tester2')
    # for result in results:
    #     print(result.members)

    # addCircle = Circle.objects.filter(name='tester1')
    # m1 = CircleMembership.objects.create(circle=addCircle, user=request.user,inviter=request.user)
    # This will give me all the circles that mcnalj ide = 1 belongs to
    results = Circle.objects.filter(members__id=1)
    for result in results:
        print(result)
    circle = Circle.objects.get(id = 1)
    """ I have the circle, this will give me a list of all its members."""
    list = circle.members.all()

    #I have the user, this gets all the circles they are members of.
    circles = request.user.circle_set.all()

    # Since I have a related_name ('circle_member') on Circle, I can use thatinstead of entry_set.
    circles = request.user.circle_member.all()

    return redirect('copacity_app:index')
