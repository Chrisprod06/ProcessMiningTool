from django.shortcuts import render

# Create your views here.


def register(request):
    return render(request, "accounts/register.html")


def login(request):
    return render(request, "accounts/login.html")


def forgot_password(request):
    return render(request, "accounts/forgot_password.html")
