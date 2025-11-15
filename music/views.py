# music/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum
from .forms import CustomUserCreationForm, AlbumForm, TrackForm
from .models import User, Album, Genre, Track
from .models import User, Album, Genre, Track, Playlist, Favorite
from .forms import CustomUserCreationForm, AlbumForm, TrackForm, PlaylistForm

def landing_page(request):
    """Landing page - головна сторінка"""
    context = {
        'total_artists': User.objects.filter(role='artist').count(),
        'total_albums': Album.objects.count(),
        'total_genres': Genre.objects.count(),
    }
    return render(request, 'music/landing.html', context)

def register_view(request):
    """Реєстрація користувачів"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Акаунт створено для {username}! Тепер ви можете увійти.')
            return redirect('music:login')
        else:
            messages.error(request, 'Помилка при реєстрації. Перевірте введені дані.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'music/register.html', {'form': form})

def login_view(request):
    """Вхід користувачів"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Вітаємо, {user.stage_name or user.username}!')

            if user.role == 'artist':
                return redirect('music:artist_dashboard')
            elif user.role == 'producer':
                return redirect('music:producer_dashboard')
            elif user.role == 'listener':
                return redirect('music:listener_home')
            elif user.role == 'manager':
                return redirect('music:manager_dashboard')
            
            return redirect('music:dashboard')
        else:
            messages.error(request, 'Невірне ім\'я користувача або пароль')
    return render(request, 'music/login.html')

@login_required
def dashboard_view(request):
    """Персональний кабінет користувача"""
    user = request.user
    
    if user.role == 'artist':
        return redirect('music:artist_dashboard')
    elif user.role == 'producer':
        return redirect('music:producer_dashboard')
    elif user.role == 'listener':
        return redirect('music:listener_home')
    elif user.role == 'manager':
        return redirect('music:manager_dashboard')
    
    return redirect('music:dashboard')

def about_view(request):
    """Сторінка про компанію"""
    return render(request, 'music/about.html')

@login_required
def profile_view(request):
    """Профіль користувача"""
    return render(request, 'music/profile.html', {'user': request.user})

# ==================== ARTIST DASHBOARD ====================
@login_required
def artist_dashboard(request):
    """Головна панель артиста"""
    if request.user.role != 'artist':
        messages.error(request, 'У вас немає доступу до цієї сторінки')
        return redirect('music:dashboard')
    
    albums = Album.objects.filter(artist=request.user)
    tracks = Track.objects.filter(album__artist=request.user)
    recent_tracks = tracks.order_by('-created_at')[:5]
    
    context = {
        'total_tracks': tracks.count(),
        'total_albums': albums.count(),
        'followers': 1234,  # Заглушка
        'plays': 45600,  # Заглушка
        'recent_tracks': recent_tracks,
    }
    return render(request, 'music/artist_dashboard.html', context)

# ==================== ALBUM CRUD ====================
@login_required
def album_list(request):
    """Список альбомів артиста"""
    if request.user.role != 'artist':
        messages.error(request, 'У вас немає доступу до цієї сторінки')
        return redirect('music:dashboard')
    
    albums = Album.objects.filter(artist=request.user).annotate(
        tracks_count=Count('tracks')
    ).order_by('-created_at')
    
    context = {'albums': albums}
    return render(request, 'music/album_list.html', context)

@login_required
def album_create(request):
    """Створення нового альбому"""
    if request.user.role != 'artist':
        messages.error(request, 'У вас немає доступу до цієї сторінки')
        return redirect('music:dashboard')
    
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.artist = request.user
            album.save()
            messages.success(request, f'Альбом "{album.title}" успішно створено!')
            return redirect('music:album_detail', pk=album.pk)
        else:
            messages.error(request, 'Помилка при створенні альбому. Перевірте введені дані.')
    else:
        form = AlbumForm()
    
    context = {'form': form, 'action': 'Створити'}
    return render(request, 'music/album_form.html', context)

@login_required
def album_detail(request, pk):
    """Детальна інформація про альбом"""
    album = get_object_or_404(Album, pk=pk, artist=request.user)
    tracks = album.tracks.all().order_by('track_number')
    
    context = {
        'album': album,
        'tracks': tracks,
    }
    return render(request, 'music/album_detail.html', context)

@login_required
def album_update(request, pk):
    """Редагування альбому"""
    album = get_object_or_404(Album, pk=pk, artist=request.user)
    
    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            messages.success(request, f'Альбом "{album.title}" успішно оновлено!')
            return redirect('music:album_detail', pk=album.pk)
        else:
            messages.error(request, 'Помилка при оновленні альбому.')
    else:
        form = AlbumForm(instance=album)
    
    context = {
        'form': form,
        'album': album,
        'action': 'Оновити'
    }
    return render(request, 'music/album_form.html', context)

@login_required
def album_delete(request, pk):
    """Видалення альбому"""
    album = get_object_or_404(Album, pk=pk, artist=request.user)
    
    if request.method == 'POST':
        album_title = album.title
        album.delete()
        messages.success(request, f'Альбом "{album_title}" успішно видалено!')
        return redirect('music:album_list')
    
    context = {'album': album}
    return render(request, 'music/album_confirm_delete.html', context)

# ==================== TRACK CRUD ====================
@login_required
def track_create(request, album_pk):
    """Додавання треку до альбому"""
    album = get_object_or_404(Album, pk=album_pk, artist=request.user)
    
    if request.method == 'POST':
        form = TrackForm(request.POST)
        if form.is_valid():
            track = form.save(commit=False)
            print(track)
            track.album = album
            track.save()
            messages.success(request, f'Трек "{track.title}" успішно додано!')
            return redirect('music:album_detail', pk=album.pk)
        else:
            messages.error(request, 'Помилка при додаванні треку.')
    else:
        # Автоматично встановлюємо наступний номер треку
        last_track = album.tracks.order_by('-track_number').first()
        initial_track_number = (last_track.track_number + 1) if last_track else 1
        form = TrackForm(initial={'track_number': initial_track_number})
    
    context = {
        'form': form,
        'album': album,
        'action': 'Додати'
    }
    return render(request, 'music/track_form.html', context)

@login_required
def track_update(request, pk):
    """Редагування треку"""
    track = get_object_or_404(Track, pk=pk, album__artist=request.user)
    
    if request.method == 'POST':
        form = TrackForm(request.POST, instance=track)
        if form.is_valid():
            form.save()
            messages.success(request, f'Трек "{track.title}" успішно оновлено!')
            return redirect('music:album_detail', pk=track.album.pk)
        else:
            messages.error(request, 'Помилка при оновленні треку.')
    else:
        form = TrackForm(instance=track)
    
    context = {
        'form': form,
        'track': track,
        'album': track.album,
        'action': 'Оновити'
    }
    return render(request, 'music/track_form.html', context)

@login_required
def track_delete(request, pk):
    """Видалення треку"""
    track = get_object_or_404(Track, pk=pk, album__artist=request.user)
    album = track.album
    
    if request.method == 'POST':
        track_title = track.title
        track.delete()
        messages.success(request, f'Трек "{track_title}" успішно видалено!')
        return redirect('music:album_detail', pk=album.pk)
    
    context = {
        'track': track,
        'album': album
    }
    return render(request, 'music/track_confirm_delete.html', context)

# ==================== OTHER DASHBOARDS ====================
@login_required
def producer_dashboard(request):
    return render(request, 'music/producer_dashboard.html')

@login_required
def listener_home(request):
    """Домашня сторінка слухача"""
    if request.user.role != 'listener':
        messages.error(request, 'У вас немає доступу до цієї сторінки')
        return redirect('music:dashboard')
    
    # Всі альбоми та треки для рекомендацій
    all_albums = Album.objects.all().select_related('artist', 'genre')[:12]
    
    # Плейлисти користувача
    user_playlists = Playlist.objects.filter(user=request.user).annotate(
        tracks_count=Count('tracks')
    )
    
    # Улюблені треки
    favorites = Favorite.objects.filter(user=request.user).select_related(
        'track__album__artist'
    )[:10]
    
    context = {
        'albums': all_albums,
        'playlists': user_playlists,
        'favorites': favorites,
    }
    return render(request, 'music/listener_home.html', context)

# ==================== PLAYLIST CRUD ====================
@login_required
def playlist_list(request):
    """Список плейлистів"""
    if request.user.role != 'listener':
        messages.error(request, 'У вас немає доступу до цієї сторінки')
        return redirect('music:dashboard')
    
    playlists = Playlist.objects.filter(user=request.user).annotate(
        tracks_count=Count('tracks')
    )
    
    context = {'playlists': playlists}
    return render(request, 'music/playlist_list.html', context)


@login_required
def playlist_create(request):
    """Створення плейлиста"""
    if request.user.role != 'listener':
        messages.error(request, 'У вас немає доступу до цієї сторінки')
        return redirect('music:dashboard')
    
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            messages.success(request, f'Плейлист "{playlist.name}" створено!')
            return redirect('music:playlist_detail', pk=playlist.pk)
    else:
        form = PlaylistForm()
    
    context = {'form': form, 'action': 'Створити'}
    return render(request, 'music/playlist_form.html', context)


@login_required
def playlist_detail(request, pk):
    """Детальна інформація про плейлист"""
    playlist = get_object_or_404(Playlist, pk=pk, user=request.user)
    tracks = playlist.tracks.all().select_related('album__artist')
    
    context = {
        'playlist': playlist,
        'tracks': tracks,
    }
    return render(request, 'music/playlist_detail.html', context)


@login_required
def playlist_update(request, pk):
    """Редагування плейлиста"""
    playlist = get_object_or_404(Playlist, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = PlaylistForm(request.POST, instance=playlist)
        if form.is_valid():
            form.save()
            messages.success(request, f'Плейлист "{playlist.name}" оновлено!')
            return redirect('music:playlist_detail', pk=playlist.pk)
    else:
        form = PlaylistForm(instance=playlist)
    
    context = {
        'form': form,
        'playlist': playlist,
        'action': 'Оновити'
    }
    return render(request, 'music/playlist_form.html', context)


@login_required
def playlist_delete(request, pk):
    """Видалення плейлиста"""
    playlist = get_object_or_404(Playlist, pk=pk, user=request.user)
    
    if request.method == 'POST':
        playlist_name = playlist.name
        playlist.delete()
        messages.success(request, f'Плейлист "{playlist_name}" видалено!')
        return redirect('music:playlist_list')
    
    context = {'playlist': playlist}
    return render(request, 'music/playlist_confirm_delete.html', context)


@login_required
def playlist_add_track(request, playlist_pk, track_pk):
    """Додати трек до плейлиста"""
    playlist = get_object_or_404(Playlist, pk=playlist_pk, user=request.user)
    track = get_object_or_404(Track, pk=track_pk)
    
    playlist.tracks.add(track)
    messages.success(request, f'Трек "{track.title}" додано до плейлиста!')
    return redirect('music:playlist_detail', pk=playlist.pk)


@login_required
def playlist_remove_track(request, playlist_pk, track_pk):
    """Видалити трек з плейлиста"""
    playlist = get_object_or_404(Playlist, pk=playlist_pk, user=request.user)
    track = get_object_or_404(Track, pk=track_pk)
    
    playlist.tracks.remove(track)
    messages.success(request, f'Трек "{track.title}" видалено з плейлиста!')
    return redirect('music:playlist_detail', pk=playlist.pk)


# ==================== FAVORITES ====================
@login_required
def toggle_favorite(request, track_pk):
    """Додати/видалити трек з улюблених"""
    track = get_object_or_404(Track, pk=track_pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, track=track)
    
    if not created:
        favorite.delete()
        messages.success(request, f'Трек "{track.title}" видалено з улюблених')
    else:
        messages.success(request, f'Трек "{track.title}" додано до улюблених')
    
    return redirect(request.META.get('HTTP_REFERER', 'music:listener_home'))


@login_required
def favorites_list(request):
    """Список улюблених треків"""
    favorites = Favorite.objects.filter(user=request.user).select_related(
        'track__album__artist'
    )
    
    context = {'favorites': favorites}
    return render(request, 'music/favorites_list.html', context)

@login_required
def manager_dashboard(request):
    return render(request, 'music/manager_dashboard.html')