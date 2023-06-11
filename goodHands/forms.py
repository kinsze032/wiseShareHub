from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Hasło"}))


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "username", "style": "font-size: 13px;"}),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Hasło", "style": "font-size: 13px;"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Powtórz hasło", "style": "font-size: 13px;"}
        )
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Imię", "style": "font-size: 13px;"}),
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Nazwisko", "style": "font-size: 13px;"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email", "style": "font-size: 13px;"})
    )

    def clean(self):
        cd = super().clean()
        pass1 = cd.get("password1")
        pass2 = cd.get("password2")
        username = cd.get("username")

        if pass1 != pass2:
            raise ValidationError("Hasła nie są identyczne")

        if username and User.objects.filter(username=username).exists():
            raise ValidationError("Username nie jest dostępny")
