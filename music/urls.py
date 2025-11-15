# music/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'music'

urlpatterns = [
    # Головні сторінки
    path('', views.landing_page, name='landing'),
    path('about/', views.about_view, name='about'),
    
    # Автентифікація
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Дашборди
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('artist/dashboard/', views.artist_dashboard, name='artist_dashboard'),
    path('producer/dashboard/', views.producer_dashboard, name='producer_dashboard'),
    path('listener/home/', views.listener_home, name='listener_home'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    
    # Профіль
    path('profile/', views.profile_view, name='profile'),
    
    # Album CRUD
    path('albums/', views.album_list, name='album_list'),
    path('albums/create/', views.album_create, name='album_create'),
    path('albums/<int:pk>/', views.album_detail, name='album_detail'),
    path('albums/<int:pk>/edit/', views.album_update, name='album_update'),
    path('albums/<int:pk>/delete/', views.album_delete, name='album_delete'),
    
    # Track CRUD
    path('albums/<int:album_pk>/tracks/create/', views.track_create, name='track_create'),
    path('tracks/<int:pk>/edit/', views.track_update, name='track_update'),
    path('tracks/<int:pk>/delete/', views.track_delete, name='track_delete'),

    # Playlist CRUD
    path('playlists/', views.playlist_list, name='playlist_list'),
    path('playlists/create/', views.playlist_create, name='playlist_create'),
    path('playlists/<int:pk>/', views.playlist_detail, name='playlist_detail'),
    path('playlists/<int:pk>/edit/', views.playlist_update, name='playlist_update'),
    path('playlists/<int:pk>/delete/', views.playlist_delete, name='playlist_delete'),
    path('playlists/<int:playlist_pk>/add/<int:track_pk>/', views.playlist_add_track, name='playlist_add_track'),
    path('playlists/<int:playlist_pk>/remove/<int:track_pk>/', views.playlist_remove_track, name='playlist_remove_track'),

    # Favorites
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('tracks/<int:track_pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),

    # Music Search
    path('search/', views.music_search, name='music_search'),
    path('tracks/<int:track_pk>/quick-add/', views.quick_add_to_playlist, name='quick_add_to_playlist'),

    # Contract CRUD
    path('contracts/', views.contract_list, name='contract_list'),
    path('contracts/create/', views.contract_create, name='contract_create'),
    path('contracts/<int:pk>/', views.contract_detail, name='contract_detail'),
    path('contracts/<int:pk>/edit/', views.contract_update, name='contract_update'),
    path('contracts/<int:pk>/delete/', views.contract_delete, name='contract_delete'),
]