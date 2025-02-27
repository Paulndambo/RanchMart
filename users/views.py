from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from users.models import User
from django.views.generic import ListView
from django.db.models import Q

GENDERS = [
    'Male',
    'Female',
]

ROLES = [
    'Caretaker',
    'House Manager',
]

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)  # Redirect to the next URL or home page.
        else:
            return redirect('login')
    next_url = request.GET.get('next', '')
    return render(request, 'accounts/login.html', {'next': next_url})

@login_required
def logout_user(request):
    logout(request)
    return redirect('login')  # Redirect to a login page.


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        gender = request.POST.get("gender")
        password = request.POST.get("password")

        user = User.objects.create(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            gender=gender,
            password=password
        )
        user.set_password(password)
        user.save()
        return redirect("login")
    return render(request, "accounts/register.html")


def users(request):
    context = {
        "users": User.objects.all()
    }
    return render(request, "accounts/users.html", context)