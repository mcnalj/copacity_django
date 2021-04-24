from django.db import models
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


class CheckIn(models.Model):
    """A daily checkIn"""
    PEOPLE = [(1, 'Jake'), (3, 'Leah'), (4, 'Raizel'), (5, 'Oscar')]
    SAFE = [(1, 'Yes'), (2, 'No'), (3, 'Maybe')]
    URGENCY = [(1, 'Call now'), (2, 'Text now'), (3, 'Talk later'), (4, 'Not necessary to talk about it'), (5, 'I Prefer not to talk about it')]
    dateTime = models.DateTimeField(auto_now_add=True)
    yourName = models.IntegerField(blank=False, default=0, choices=PEOPLE)
    hardToday = models.CharField(max_length=200)
    goodToday = models.CharField(max_length=200)
    excitedToday = models.CharField(max_length=200)
    thoughts = models.IntegerField(blank=False, default=0, choices=SAFE)
    thoughtsExplained = models.CharField(max_length=400)
    actions = models.IntegerField(blank=False, default=0, choices=SAFE)
    actionsExplained = models.CharField(max_length=400)
    moodRange = models.IntegerField(blank=False, default=5)
    pintaRange = models.IntegerField(blank=False, default=5)
    urgency = models.IntegerField(default=4, choices=URGENCY)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

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
