# music/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Genre, Album, Track

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Адмін панель для користувачів"""
    list_display = ('username', 'email', 'role', 'stage_name', 'is_staff', 'created_at')
    list_filter = ('role', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('username', 'email', 'stage_name')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Додatkova інформація', {
            'fields': ('role', 'stage_name', 'bio')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Додatkova інформація', {
            'fields': ('email', 'role', 'stage_name', 'bio')
        }),
    )

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Адмін панель для жанрів"""
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    """Адмін панель для альбомів"""
    list_display = ('title', 'artist', 'genre', 'release_date', 'created_at')
    list_filter = ('genre', 'release_date', 'created_at')
    search_fields = ('title', 'artist__username', 'artist__stage_name')
    ordering = ('-created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('artist', 'genre')

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    """Адмін панель для треків"""
    list_display = ('title', 'album', 'track_number', 'duration')
    list_filter = ('album__genre', 'album__release_date')
    search_fields = ('title', 'album__title')
    ordering = ('album', 'track_number')

# Налаштування заголовків адмін панелі
admin.site.site_header = 'MusicHub Ukraine - Адміністрування'
admin.site.site_title = 'MusicHub Admin'
admin.site.index_title = 'Панель управління'