from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views import View

from goodHands.forms import LoginForm, RegisterForm
from goodHands.models import Donation, Institution


User = get_user_model()


class LandingPageView(View):
    template_name = "goodHands/index.html"

    def get(self, request):
        total_bags = Donation.objects.aggregate(Sum("quantity"))["quantity__sum"]
        total_institutions = Donation.objects.values("institution").count()

        typy = ["fundacja", "organizacja", "zbiórka"]
        fund_institutions = (
            Institution.objects.filter(type=typy[0]).prefetch_related("categories").order_by("name")
        )
        non_gov_institutions = (
            Institution.objects.filter(type=typy[1]).prefetch_related("categories").order_by("name")
        )
        loc_col_institutions = (
            Institution.objects.filter(type=typy[2]).prefetch_related("categories").order_by("name")
        )

        context = {
            'total_bags': total_bags,
            'total_institutions': total_institutions,
            'fund_institutions': fund_institutions,
            'non_gov_institutions': non_gov_institutions,
            'loc_col_institutions': loc_col_institutions,
        }
        return render(request, self.template_name, context)


class AddDonationView(View):
    template_name = "goodHands/form.html"

    def get(self, request):
        return render(request, self.template_name)


class LoginView(View):
    template_name = "goodHands/login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Znajdź użytkownika na podstawie adresu e-mail
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('landing_page')
            else:
                return redirect('register')
        return render(request, self.template_name, {"form": form})


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('landing_page')


class RegisterView(View):
    template_name = "goodHands/register.html"
    form_class = RegisterForm

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password1 = form.cleaned_data["password1"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]

            User.objects.create_user(
                username=username,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            return redirect("login")

        else:
            return render(request, self.template_name, {"form": form})
