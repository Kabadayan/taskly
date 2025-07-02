# Handles rendering templates and redirecting users
from django.shortcuts import render, redirect
# Provides authentication functions like login and logout
from django.contrib.auth import authenticate, login, logout
# Decorator to require login for function-based views
from django.contrib.auth.decorators import login_required
# Mixin to require login for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
# Base class for creating class-based views
from django.views import View
# Django's built-in User model
from django.contrib.auth.models import User
# Custom registration form
from .forms import RegisterForm

def register_view(request):
    """
    Handles user registration. On POST, it validates the form, creates the user,
    logs them in, and redirects to the index page. On GET, it renders an empty form.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('index_page')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """
    Handles user login. On POST, it authenticates the user and logs them in.
    Redirects to 'next' URL if provided or to the index page. On failure, shows an error.
    On GET, renders the login form.
    """
    error_message = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'index_page'
            return redirect(next_url)
        else:
            error_message = "Invalid Credentials!"
    return render(request, 'accounts/login.html', {'error': error_message})

def logout_view(request):
    """
    Handles user logout. Only accepts POST requests for security.
    After logout, redirects to the index page. Redirects even on non-POST for safety.
    """
    if request.method == "POST":
        logout(request)
        return redirect('index_page')
    else:
        return redirect('index_page')