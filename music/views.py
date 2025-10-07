# music/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import User, Album, Genre

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

            # Перенаправлення залежно від ролі
            if user.role == 'artist':
                return redirect('music:artist_dashboard')  # окремий dashboard для артиста
            elif user.role == 'producer':
                return redirect('music:producer_dashboard')
            elif user.role == 'listener':
                return redirect('music:listener_home')
            elif user.role == 'manager':
                return redirect('music:manager_dashboard')
            
            # fallback
            return redirect('music:dashboard')

        else:
            messages.error(request, 'Невірне ім\'я користувача або пароль')
    return render(request, 'music/login.html')

@login_required
def dashboard_view(request):
    """Персональний кабінет користувача"""
    user = request.user
    context = {
        'user': user,
        'role_display': user.get_role_display(),
    }
    
    # Додаткова інформація залежно від ролі
    if user.role == 'artist':
        context['albums'] = Album.objects.filter(artist=user)
        context['albums_count'] = context['albums'].count()
    elif user.role == 'admin':
        context['total_users'] = User.objects.count()
        context['total_albums'] = Album.objects.count()
        context['total_genres'] = Genre.objects.count()
        context['recent_users'] = User.objects.order_by('-created_at')[:5]
    elif user.role == 'producer':
        # Тут можна додати логіку для продюсерів
        context['collaborations'] = Album.objects.all()[:5]  # Заглушка
    
    # Перенаправлення залежно від ролі
    if user.role == 'artist':
        return redirect('music:artist_dashboard')  # окремий dashboard для артиста
    elif user.role == 'producer':
        return redirect('music:producer_dashboard')
    elif user.role == 'listener':
        return redirect('music:listener_home')
    elif user.role == 'manager':
        return redirect('music:manager_dashboard')
    
    # fallback
    return redirect('music:dashboard')

def about_view(request):
    """Сторінка про компанію"""
    return render(request, 'music/about.html')

@login_required
def profile_view(request):
    """Профіль користувача"""
    return render(request, 'music/profile.html', {'user': request.user})

@login_required
def artist_dashboard(request):
    # Логіка артиста
    return render(request, 'music/artist_dashboard.html')

@login_required
def producer_dashboard(request):
    # Логіка продюсера
    return render(request, 'music/producer_dashboard.html')

@login_required
def listener_home(request):
    # Логіка слухача
    return render(request, 'music/listener_home.html')

@login_required
def manager_dashboard(request):
    # Логіка менеджера
    return render(request, 'music/manager_dashboard.html')