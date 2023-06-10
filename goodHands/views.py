from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from goodHands.models import Donation, Institution


class LandingPageView(View):
    template_name = 'goodHands/index.html'

    def get(self, request):
        total_bags = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        total_institutions = Donation.objects.values('institution').count()

        typy = ['fundacja', 'organizacja', 'zbiórka']
        fund_institutions = Institution.objects.filter(type=typy[0]).prefetch_related('categories')
        non_gov_institutions = Institution.objects.filter(type=typy[1]).prefetch_related('categories')
        loc_col_institutions = Institution.objects.filter(type=typy[2]).prefetch_related('categories')

        context = {
            'total_bags': total_bags,
            'total_institutions': total_institutions,
            'fund_institutions': fund_institutions,
            'non_gov_institutions': non_gov_institutions,
            'loc_col_institutions': loc_col_institutions,
        }
        return render(request, self.template_name, context)


class AddDonationView(View):
    template_name = 'goodHands/form.html'

    def get(self, request):
        return render(request, self.template_name)


class LoginView(View):
    template_name = 'goodHands/login.html'

    def get(self, request):
        return render(request, self.template_name)


class RegisterView(View):
    template_name = 'goodHands/register.html'

    def get(self, request):
        return render(request, self.template_name)
