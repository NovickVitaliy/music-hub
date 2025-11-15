# music/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Розширена модель користувача для музичної індустрії"""
    USER_ROLES = (
        ('admin', 'Administrator'),
        ('artist', 'Artist'),
        ('producer', 'Producer'),
        ('listener', 'Listener'),
        ('label_manager', 'Label Manager'),
    )
    
    role = models.CharField(max_length=20, choices=USER_ROLES, default='listener')
    bio = models.TextField(blank=True, null=True)
    stage_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Genre(models.Model):
    """Музичні жанри"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Album(models.Model):
    """Альбоми"""
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'artist'})
    release_date = models.DateField()
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.artist.stage_name or self.artist.username}"

class Track(models.Model):
    """Треки (для майбутнього розвитку)"""
    title = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')
    duration = models.DurationField(null=True, blank=True)
    track_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['track_number']
        unique_together = ['album', 'track_number']
    
    def __str__(self):
        return f"{self.track_number}. {self.title}"
    
    def get_duration_display(self):
        """Повертає відформатовану тривалість"""
        if self.duration:
            total_seconds = int(self.duration.total_seconds())
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            return f"{minutes}:{seconds:02d}"
        return "0:00"
    
class Playlist(models.Model):
    """Плейлисти слухачів"""
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'listener'})
    description = models.TextField(blank=True)
    tracks = models.ManyToManyField(Track, related_name='playlists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
    def get_total_duration(self):
        """Загальна тривалість плейлиста"""
        from datetime import timedelta
        total = timedelta()
        for track in self.tracks.all():
            if track.duration:
                total += track.duration
        return total
    
    def get_duration_display(self):
        """Форматована тривалість"""
        duration = self.get_total_duration()
        hours = int(duration.total_seconds() // 3600)
        minutes = int((duration.total_seconds() % 3600) // 60)
        return f"{hours} год {minutes} хв"


class Favorite(models.Model):
    """Улюблені треки"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'track']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.track.title}"
    
class Contract(models.Model):
    """Контракти з артистами"""
    CONTRACT_TYPES = (
        ('exclusive', 'Ексклюзивний реліз'),
        ('distribution', 'Дистрибуція альбому'),
        ('long_term', 'Довгострокова співпраця'),
    )
    
    STATUS_CHOICES = (
        ('active', 'Активний'),
        ('expiring', 'Закінчується'),
        ('pending', 'На розгляді'),
        ('expired', 'Закінчився'),
    )
    
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_contracts', limit_choices_to={'role': 'label_manager'})
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contracts', limit_choices_to={'role': 'artist'})
    contract_type = models.CharField(max_length=20, choices=CONTRACT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Фінансові умови
    artist_royalty_percent = models.DecimalField(max_digits=5, decimal_places=2, help_text="Процент для артиста")
    label_royalty_percent = models.DecimalField(max_digits=5, decimal_places=2, help_text="Процент для лейблу")
    
    # Терміни
    duration_months = models.PositiveIntegerField(help_text="Тривалість у місяцях")
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Додаткова інформація
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True, help_text="Додаткові примітки")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.artist.stage_name or self.artist.username} - {self.get_contract_type_display()}"
    
    def months_remaining(self):
        """Скільки місяців залишилось до закінчення"""
        from datetime import date
        from dateutil.relativedelta import relativedelta
        
        today = date.today()
        if self.end_date < today:
            return 0
        
        delta = relativedelta(self.end_date, today)
        return delta.years * 12 + delta.months
    
    def save(self, *args, **kwargs):
        # Автоматично оновлюємо статус
        if self.months_remaining() == 0:
            self.status = 'expired'
        elif self.months_remaining() <= 3 and self.status == 'active':
            self.status = 'expiring'
        
        super().save(*args, **kwargs)