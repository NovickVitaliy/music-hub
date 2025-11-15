# music/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Contract, Playlist, User, Album, Track, Genre

class CustomUserCreationForm(UserCreationForm):
    """Форма реєстрації з додатковими полями"""
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[
        ('artist', 'Artist'),
        ('producer', 'Producer'),
        ('listener', 'Listener'),
        ('label_manager', 'Label Manager'),
    ])
    stage_name = forms.CharField(
        max_length=100, 
        required=False, 
        help_text="Для артистів та продюсерів",
        widget=forms.TextInput(attrs={'placeholder': 'Введіть сценічне ім\'я'})
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Розкажіть про себе...'}), 
        required=False,
        label="Біографія"
    )
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role", "stage_name", "bio")
        labels = {
            'username': 'Ім\'я користувача',
            'email': 'Електронна пошта',
            'password1': 'Пароль',
            'password2': 'Підтвердження пароля',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Введіть ім\'я користувача'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@email.com'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.role = self.cleaned_data["role"]
        user.stage_name = self.cleaned_data["stage_name"]
        user.bio = self.cleaned_data["bio"]
        if commit:
            user.save()
        return user


class AlbumForm(forms.ModelForm):
    """Форма для створення/редагування альбому"""
    
    class Meta:
        model = Album
        fields = ['title', 'genre', 'release_date', 'description']
        labels = {
            'title': 'Назва альбому',
            'genre': 'Жанр',
            'release_date': 'Дата релізу',
            'description': 'Опис',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть назву альбому'
            }),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Опишіть ваш альбом...'
            }),
        }


class TrackForm(forms.ModelForm):
    """Форма для створення/редагування треку"""
    
    duration_minutes = forms.IntegerField(
        min_value=0,
        required=False,
        label='Хвилини',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0'
        })
    )
    duration_seconds = forms.IntegerField(
        min_value=0,
        max_value=59,
        required=False,
        label='Секунди',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0'
        })
    )
    
    class Meta:
        model = Track
        fields = ['title', 'track_number']
        labels = {
            'title': 'Назва треку',
            'track_number': 'Номер треку',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть назву треку'
            }),
            'track_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.duration:
            total_seconds = int(self.instance.duration.total_seconds())
            self.fields['duration_minutes'].initial = total_seconds // 60
            self.fields['duration_seconds'].initial = total_seconds % 60
    
    def save(self, commit=True):
        track = super().save(commit=False)
        minutes = self.cleaned_data.get('duration_minutes') or 0
        seconds = self.cleaned_data.get('duration_seconds') or 0
        
        from datetime import timedelta
        track.duration = timedelta(minutes=minutes, seconds=seconds)
        
        if commit:
            track.save()
        return track
    
class PlaylistForm(forms.ModelForm):
    """Форма для створення/редагування плейлиста"""
    
    class Meta:
        model = Playlist
        fields = ['name', 'description']
        labels = {
            'name': 'Назва плейлиста',
            'description': 'Опис',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть назву плейлиста'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Опис плейлиста (необов\'язково)'
            }),
        }

class ContractForm(forms.ModelForm):
    """Форма для створення/редагування контракту"""
    
    class Meta:
        model = Contract
        fields = ['artist', 'contract_type', 'status', 'artist_royalty_percent', 
                  'label_royalty_percent', 'duration_months', 'start_date', 'description', 'notes']
        labels = {
            'artist': 'Артист',
            'contract_type': 'Тип контракту',
            'status': 'Статус',
            'artist_royalty_percent': 'Роялті артиста (%)',
            'label_royalty_percent': 'Роялті лейблу (%)',
            'duration_months': 'Тривалість (місяців)',
            'start_date': 'Дата початку',
            'description': 'Опис',
            'notes': 'Примітки',
        }
        widgets = {
            'artist': forms.Select(attrs={'class': 'form-control'}),
            'contract_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'artist_royalty_percent': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'label_royalty_percent': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'duration_months': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показуємо тільки артистів
        self.fields['artist'].queryset = User.objects.filter(role='artist')
    
    def clean(self):
        cleaned_data = super().clean()
        artist_percent = cleaned_data.get('artist_royalty_percent', 0)
        label_percent = cleaned_data.get('label_royalty_percent', 0)
        
        if artist_percent + label_percent != 100:
            raise forms.ValidationError(
                'Сума роялті артиста та лейблу повинна дорівнювати 100%'
            )
        
        return cleaned_data
    
    def save(self, commit=True):
        contract = super().save(commit=False)
        
        # Автоматично розраховуємо дату закінчення
        from dateutil.relativedelta import relativedelta
        contract.end_date = contract.start_date + relativedelta(months=contract.duration_months)
        
        if commit:
            contract.save()
        return contract