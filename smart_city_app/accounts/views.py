from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ParkingUser
from .forms import ParkingUserRegistrationForm, ParkingUserLoginForm
from django.utils.decorators import method_decorator
from functools import wraps
from django.shortcuts import render
from firebase_admin import firestore
from django.views.decorators.http import require_POST
from django.http import HttpResponse

db = firestore.client()


def booking_success(request):
    return render(request, 'accounts/booking_success.html')

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


def book_spot(request, spot_id):
    # Access the Firebase 'smart parking lot' collection
    spot_ref = db.collection('smart-parking-lot').document(str(spot_id))
    spot = spot_ref.get()

    if spot.exists:
        spot_data = spot.to_dict()
        spot_data['id'] = int(spot.id)
        context = {
            'spot': spot_data
        }
        return render(request, 'accounts/book_spot.html', context)
    else:
        return render(request, 'accounts/error.html', {"message": "Spot not found"})

@require_POST
def confirm_book_spot(request, spot_id):
    spot_ref = db.collection('smart-parking-lot').document(str(spot_id))
    spot = spot_ref.get()
    
    if not spot.exists:
        return HttpResponse("Parking spot not found.", status=404)

    # Retrieve the current capacity
    spot_data = spot.to_dict()
    current_capacity = int(spot_data.get("capacity", 0))

    # Check if there's availability
    if current_capacity > 0:
        # Decrease the count by 1
        new_capacity = current_capacity - 1
        spot_ref.update({"capacity": new_capacity})

        # Redirect to a confirmation page or back to the details
        return redirect('booking_success')  # Replace 'booking_success' with your success page
    else:
        return HttpResponse("No spots available.", status=400)




@custom_login_required
def home(request):
    return render(request, 'accounts/home.html')