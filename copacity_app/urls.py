"""Defines URL patterns for copacity_app."""
from django.urls import path

from . import views

app_name = 'copacity_app'
urlpatterns = [
  # Home Page
  path('', views.index, name='index'),
  # Page that allows you to check in.
  #path('checkIn/', views.checkIn, name='checkIn'),
  # Page the shows all checkIns or all checkIns for any person.
  path('checkIns/<int:nameId>/', views.checkIns, name='checkIns'),
  # Page to add a new checkIn.
  path('new_checkIn/', views.new_checkIn, name='new_checkIn'),
]
