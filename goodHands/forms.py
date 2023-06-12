from django import forms
from django.core.exceptions import ValidationError
from .models import User


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=128,
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Hasło"}))


class RegisterForm(forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Hasło", "style": "font-size: 13px;"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Powtórz hasło", "style": "font-size: 13px;"}
        )
    )
    first_name = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={"placeholder": "Imię", "style": "font-size: 13px;"}),
    )
    last_name = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={"placeholder": "Nazwisko", "style": "font-size: 13px;"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email", "style": "font-size: 13px;"})
    )

    def clean(self):
        cd = super().clean()
        pass1 = cd.get("password1")
        pass2 = cd.get("password2")
        email = cd.get("email")

        if pass1 != pass2:
            raise ValidationError("Hasła nie są identyczne")

        if email and User.objects.filter(email=email).exists():
            raise ValidationError("Email nie jest dostępny")
