from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Response(models.Model):
    """A response to the daily check-in. This can be deleted."""
    dateTime = models.DateTimeField(auto_now_add=True)
    yourName = models.IntegerField(blank=False, default=0)
    hardToday = models.CharField(max_length=200)
    goodToday = models.CharField(max_length=200)
    excitedToday = models.CharField(max_length=200)
    suicideRadio = models.IntegerField(blank=False, default=0)
    moodRange = models.IntegerField(blank=False, default=0)
    pintaRange = models.IntegerField(blank=False, default=0)

    def __str__(self):
        """Return a string representation of the model."""
        message = "Person: " + str(self.yourName) + " Mood: " + str(self.moodRange)
        return message



class Circle(models.Model):
    """A Circle"""
    name = models.CharField(max_length=50)
    adminId = models.ForeignKey(User, on_delete=models.CASCADE)
    createdBy = models.CharField(max_length=50)
    createdOn = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(
        User,
        through='CircleMembership',
        through_fields=('circle', 'user'),
        related_name='circle_member',
        blank=True,
        null=True
    )

    def __str__(self):
        """Return a string representation of the model."""
        message = self.name
        return message


class CircleMembership(models.Model):
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='circle_invites')

    def __str__(self):
        """Return a string representation of the model."""
        message = str(self.circle) + " member = " + str(self.user)
        return message


class CheckIn(models.Model):
    """A daily checkIn"""
    PEOPLE = [(1, 'Jake'), (2, 'Leah'), (3, 'Raizel'), (4, 'Oscar')]
    SAFE = [(1, 'Yes'), (2, 'No'), (3, 'Maybe')]
    URGENCY = [(1, 'Call now'), (2, 'Text now'), (3, 'Talk later'), (4, 'Not necessary to talk about it'), (5, 'I Prefer not to talk about it')]
#    CIRCLES = [(0, 'none'), (1, 'monopoly'), (2, 'kids')]
    dateTime = models.DateTimeField(auto_now_add=True)
    yourName = models.IntegerField(blank=False, default=0, choices=PEOPLE)
    hardToday = models.CharField(max_length=200)
    goodToday = models.CharField(max_length=200)
    excitedToday = models.CharField(max_length=200)
    thoughts = models.IntegerField(blank=False, default=0, choices=SAFE)
    thoughtsExplained = models.CharField(blank=True, null=True, default='', max_length=400)
    actions = models.IntegerField(blank=False, default=0, choices=SAFE)
    actionsExplained = models.CharField(blank=True, null=True, default='', max_length=400)
    moodRange = models.IntegerField(blank=False, default=5)
    pintaRange = models.IntegerField(blank=False, default=5)
    urgency = models.IntegerField(default=4, choices=URGENCY)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #visibility = models.IntegerField(blank=False, default=0, choices=CIRCLES)
    visibility = models.ManyToManyField(Circle, related_name='visibility', blank=True, null=True)


    def __str__(self):
        """Return a string representation of the model."""
        name = ""
        if self.yourName == 1:
            name = "Jake"
        if self.yourName == 2:
            name = "Leah"
        if self.yourName == 3:
            name = "Raizel"
        if self.yourName == 4:
            name = "Oscar"

        message = "Name: " + name + ", Good: " + self.goodToday + ", Hard: " + self.hardToday  + ", Mood: " + str(self.moodRange) + ", Urgency: " + str(self.urgency)
        return message

class CircleMembership_Inline(admin.TabularInline):
    model=CircleMembership
    extra=1

class circleAdmin(admin.ModelAdmin):
    inlines = (CircleMembership_Inline,)
    readonly_fields = ('id',)

class usersAdmin(admin.ModelAdmin):
    inlines = (CircleMembership_Inline,)
