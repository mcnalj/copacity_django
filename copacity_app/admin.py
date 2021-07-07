from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import Response
from .models import CheckIn
from .models import Circle
from .models import CircleMembership
from .models import circleAdmin
from .models import usersAdmin


admin.site.register(Response)
admin.site.register(CheckIn)
admin.site.register(Circle, circleAdmin)
admin.site.register(CircleMembership)
