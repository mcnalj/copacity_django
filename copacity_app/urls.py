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
  #path('checkIns/<int:nameId>/', views.checkIns, name='checkIns'),
  # Page to add a new checkIn.
  path('new_checkIn/', views.new_checkIn, name='new_checkIn'),
  # Page to view all your checkIns.
  path('yourCheckIns/', views.yourCheckIns, name = 'yourCheckIns'),
  # Page to view your circles and their checkins.
  path('yourCircles/', views.yourCircles, name = 'yourCircles'),
  # Page to manage circles.
  path('manage_circles/', views.manage_circles, name = 'manage_circles'),
  # Page to add members to a circle.
  path('add_mtm/', views.add_mtm, name = 'add_mtm'),
  # Page to create a circle.
  path('createCircle/', views.createCircle, name = 'createCircle'),
  # Page to select a circle to manage.
  path('manage_circles/', views.manage_circles, name = 'manage_circles'),
  # Page to add or remove members of a circle.
  path('edit_circles/', views.edit_circles, name = 'edit_circles'),
  # Page to view all of a circle's checkins.
  path('circles_checkins/', views.circles_checkins, name = 'circles_checkins'),
  # Page to view all of a circle's checkins from the Your circles page. Added to fix error
  path('circles_checkins_view/', views.circles_checkins_view, name = 'circles_checkins_view'),
  # Page to view all of a circle's checkins from the Your circles page.

  path('circles_checkins_view/<int:circleId>', views.circles_checkins_view, name = 'circles_checkins_view'),
  # Page to view a circle's details from yourCircles page.
  path('circle_details/<int:circleId>', views.circle_details, name = 'circle_details'),
  # Page to perform the update of editted circles.
  path('save_editted_circles/', views.save_editted_circles, name = 'save_editted_circles'),
  # Page to practice the updating a circle.
  path('update_circle/', views.update_circle, name = 'update_circle'),
  # Page to fill in the parameters to request a check-in.
  path('request_checkin/', views.request_checkin, name = 'request_checkin'),
  # Logic to send a SMS to request a check-in.
  path('send_checkin_request/', views.send_checkin_request, name = 'send_checkin_request'),

]
