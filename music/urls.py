# music/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('about/', views.about_view, name='about'),
    path('profile/', views.profile_view, name='profile'),
    path('artist/dashboard/', views.artist_dashboard, name='artist_dashboard'),
    path('producer/dashboard/', views.producer_dashboard, name='producer_dashboard'),
    path('listener/home/', views.listener_home, name='listener_home'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
]