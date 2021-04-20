from django.contrib import admin

# Register your models here.
from .models import Response
from .models import CheckIn

admin.site.register(Response)
admin.site.register(CheckIn)
