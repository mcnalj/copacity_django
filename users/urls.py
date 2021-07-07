"""Defines URL patterns for users"""

from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'
urlpatterns = [
    # Include default auth urls.
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    path('register/', views.register, name='register'),
    # Profile update page.
    path('profile/', views.profile, name='profile'),
    # Change password
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('users:password_change_done')), name='password_change'),
]
