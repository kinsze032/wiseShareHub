from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView

from goodHands.forms import LoginForm, DonationForm, UserCreationForm
from goodHands.models import Donation, Institution, Category

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

        categories = Category.objects.all()

        context = {
            'total_bags': total_bags['total_quantity'],
            'total_institutions': total_institutions,
            'fund_institutions': fund_institutions,
            'non_gov_institutions': non_gov_institutions,
            'loc_col_institutions': loc_col_institutions,
            'categories': categories,
        }
        return render(request, self.template_name, context)


class AddDonationView(View):
    template_name = "goodHands/form.html"

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()

        context = {
            'categories': categories,
            'institutions': institutions,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = request.user
            categories = form.cleaned_data.get('categories')
            donation.save()

            if categories:
                donation.categories.set(categories)

            return JsonResponse({'url': reverse('form-confirmation')})

        return JsonResponse({'url': reverse('add_donation')})


class FormConfirmationView(View):
    template_name = "goodHands/form-confirmation.html"

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


class RegisterView(CreateView):
    template_name = "goodHands/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        return HttpResponseRedirect(self.success_url)


class UserProfileView(View):
    template_name = "goodHands/user-profile.html"

    def get(self, request):
        user = request.user
        donations = Donation.objects.filter(user=user)

        context = {
            'user': user,
            'donations': donations,
        }

        return render(request, self.template_name, context)
