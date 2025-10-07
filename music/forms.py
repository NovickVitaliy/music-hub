# music/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

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
        # Додаємо CSS класи для стилізації
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