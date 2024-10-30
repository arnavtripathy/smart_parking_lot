from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ParkingUser
from .forms import ParkingUserRegistrationForm, ParkingUserLoginForm
from django.utils.decorators import method_decorator
from functools import wraps


def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request, "You need to log in to access this page.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def register_view(request):
    if request.method == 'POST':
        form = ParkingUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = ParkingUserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = ParkingUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = ParkingUser.objects.get(username=username, password=password)
                request.session['user_id'] = user.id  # Store user ID in session
                messages.success(request, "Logged in successfully!")
                return redirect('home')
            except ParkingUser.DoesNotExist:
                messages.error(request, "Invalid username or password")
    else:
        form = ParkingUserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']  # Clear the user session
    messages.success(request, "Logged out successfully!")
    return redirect('login')

@custom_login_required
def home(request):
    return render(request, 'accounts/home.html')