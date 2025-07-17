from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email Adresi',
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
        )
    first_name = forms.CharField(
        max_length=150,
        required=True, 
        label='Adınız',
        widget=forms.TextInput(attrs={'placeholder': 'Adınız'})
        )
    last_name = forms.CharField(
        max_length=150, 
        required=True, 
        label='Soyadınız',
        widget=forms.TextInput(attrs={'placeholder': 'Soyadınız'})
        )


    class Meta(UserCreationForm.Meta):
        model = CustomUser  
        fields = ('username', 'email', 'first_name', 'last_name',)

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Kullanıcı Adı', 'class': 'text-input'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Şifre', 'class': 'password-input'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Şifre Tekrar', 'class': 'password-input'}),
        }


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Kullanıcı adı', 'class': 'text-input'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Şifre', 'class': 'password-input'})

