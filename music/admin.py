# music/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Genre, Album, Track
from .models import User, Genre, Album, Track, Playlist, Favorite, Contract

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


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'user__username')
    filter_horizontal = ('tracks',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'track__title')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('artist', 'manager', 'contract_type', 'status', 'start_date', 'end_date', 'months_remaining')
    list_filter = ('status', 'contract_type', 'start_date')
    search_fields = ('artist__username', 'artist__stage_name', 'manager__username')
    date_hierarchy = 'start_date'
    
    def months_remaining(self, obj):
        return obj.months_remaining()
    months_remaining.short_description = 'Місяців залишилось'

from .models import User, Genre, Album, Track, Playlist, Favorite, Contract, Beat, Collaboration

@admin.register(Beat)
class BeatAdmin(admin.ModelAdmin):
    list_display = ('title', 'producer', 'genre', 'bpm', 'price', 'plays_count', 'is_available', 'created_at')
    list_filter = ('genre', 'is_available', 'is_exclusive', 'created_at')
    search_fields = ('title', 'producer__username', 'producer__stage_name')
    ordering = ('-created_at',)


@admin.register(Collaboration)
class CollaborationAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'producer', 'artist', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'created_at', 'deadline')
    search_fields = ('project_name', 'producer__username', 'artist__username')
    ordering = ('-created_at',)

# Налаштування заголовків адмін панелі
admin.site.site_header = 'MusicHub Ukraine - Адміністрування'
admin.site.site_title = 'MusicHub Admin'
admin.site.index_title = 'Панель управління'