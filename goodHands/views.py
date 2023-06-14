from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect
from django.views import View

from goodHands.forms import LoginForm, RegisterForm
from goodHands.models import Donation, Institution


User = get_user_model()


class LandingPageView(View):
    template_name = "goodHands/index.html"

    def get(self, request):
        total_bags = Donation.objects.aggregate(total_quantity=Coalesce(Sum("quantity"), 0))
        total_institutions = Donation.objects.values("institution").distinct().count()

        typy = ["fundacja", "organizacja", "zbiórka"]
        fund_institutions = (
            Institution.objects.filter(type=typy[0]).order_by("name")
        )
        non_gov_institutions = (
            Institution.objects.filter(type=typy[1]).order_by("name")
        )
        loc_col_institutions = (
            Institution.objects.filter(type=typy[2]).order_by("name")
        )

        context = {
            'total_bags': total_bags['total_quantity'],
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

            user = authenticate(request, email=email, password=password)

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
            email = form.cleaned_data["email"]
            password1 = form.cleaned_data["password1"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            User.objects.create_user(
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
            )
            return redirect("login")

        else:
            return render(request, self.template_name, {"form": form})
