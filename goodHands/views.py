from django.shortcuts import render


def landing_page(request):
    return render(request, 'goodHands/index.html')


def add_donation(request):
    return render(request, 'goodHands/form.html')


def login(request):
    return render(request, 'goodHands/login.html')


def register(request):
    return render(request, 'goodHands/register.html')
