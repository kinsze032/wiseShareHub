from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Donation

User = get_user_model()


class UserCreationForm(BaseUserCreationForm):

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

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        user = User.objects.filter(email=email)
        if user.count():
            raise ValidationError("Email already exists")
        return email

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ("email",)


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=128,
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Hasło"}))


# class RegisterForm(forms.Form):
#     password1 = forms.CharField(
#         widget=forms.PasswordInput(attrs={"placeholder": "Hasło", "style": "font-size: 13px;"})
#     )
#     password2 = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={"placeholder": "Powtórz hasło", "style": "font-size: 13px;"}
#         )
#     )
#     first_name = forms.CharField(
#         max_length=128,
#         widget=forms.TextInput(attrs={"placeholder": "Imię", "style": "font-size: 13px;"}),
#     )
#     last_name = forms.CharField(
#         max_length=128,
#         widget=forms.TextInput(attrs={"placeholder": "Nazwisko", "style": "font-size: 13px;"}),
#     )
#     email = forms.EmailField(
#         widget=forms.EmailInput(attrs={"placeholder": "Email", "style": "font-size: 13px;"})
#     )
#
#     def clean(self):
#         cd = super().clean()
#         pass1 = cd.get("password1")
#         pass2 = cd.get("password2")
#         email = cd.get("email")
#
#         if pass1 != pass2:
#             raise ValidationError("Hasła nie są identyczne")
#
#         if email and User.objects.filter(email=email).exists():
#             raise ValidationError("Email nie jest dostępny")


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = [
            "quantity",
            "categories",
            "institution",
            "address",
            "phone_number",
            "city",
            "zip_code",
            "pick_up_date",
            "pick_up_time",
            "pick_up_comment",
        ]
        exclude = ['user']
