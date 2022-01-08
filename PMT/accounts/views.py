from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth


# Create your views here.


def register(request):
    """Function for handing user registration"""
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        username = email
        password = request.POST["password"]
        repeat_password = request.POST["repeat_password"]

        # Check if password is same with repeat password, and email is unique then continue
        if password != repeat_password:
            messages.info(request, "Passwords must match!")
            return redirect('/accounts/register')
        else:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists!")
                return redirect('/accounts/register')
            else:
                user = User.objects.create_user(username=username, password=password, email=email,
                                                first_name=first_name,
                                                last_name=last_name)
                user.save()
                messages.info(request, "Account created successfully!")
                return redirect('/accounts/login')
    else:
        return render(request, "accounts/register.html")


def login(request):
    """Function for handling user login"""
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = auth.authenticate(username=email, password=password)

        if user is None:
            messages.info(request, "Wrong credentials!Please try again.")
            return redirect("/accounts/login")

        else:
            auth.login(request, user)
            return redirect("/")

    return render(request, "accounts/login.html")


def forgot_password(request):
    return render(request, "accounts/forgot_password.html")


def logout(request):
    """Function for logging out the user"""
    auth.logout(request)
    return redirect("/accounts/login")
