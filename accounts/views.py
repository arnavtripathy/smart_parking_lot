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
from uuid import uuid4
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO
import qrcode
from reportlab.lib.utils import ImageReader
from datetime import datetime

db = firestore.client()


def booking_success(request):
    # Retrieve ticket_id and car_number from query parameters
    ticket_id = request.GET.get('ticket_id')
    car_number = request.GET.get('car_number')

    # Check if required parameters are missing
    if not ticket_id or not car_number:
        return HttpResponse("Invalid or incomplete booking details.", status=400)

    # Pass the values to the template
    context = {
        "ticket_id": ticket_id,
        "car_number": car_number,
    }
    return render(request, 'accounts/booking_success.html', context)

def download_ticket(request, ticket_id, car_number):
    # Get the current date and time
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%I:%M %p")


    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
  
    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(3)
    c.rect(30, 500, 550, 250)

    
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(300, 770, "Dublin Parking Spot Booking Ticket")

    
    c.setFont("Helvetica", 14)
    c.setFillColor(colors.black)
    c.drawString(50, 700, f"Ticket ID: {ticket_id}")
    c.drawString(50, 680, f"Car Number: {car_number}")
    c.drawString(50, 660, "Thank you for booking your parking spot!")

  
    data = [
        ["Field", "Value"],
        ["Ticket ID", ticket_id],
        ["Car Number", car_number],
        ["Date", date],
        ["Time", time]
    ]
    table = Table(data, colWidths=[150, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    table.wrapOn(c, 50, 620)
    table.drawOn(c, 50, 540)

    # Generate a QR code
    qr_data = f"Ticket ID: {ticket_id}, Car Number: {car_number}"
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill="black", back_color="white")

   
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)
    qr_image = ImageReader(qr_buffer)

 
    c.drawImage(qr_image, 450, 630, width=100, height=100)


    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(300, 50, "Please present this ticket with the QR code for verification.")

    c.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=ticket_{ticket_id}.pdf'
    return response

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
    user_id = request.session.get('user_id')
    spot_ref = db.collection('smart-parking-lot').document(str(spot_id))
    spot = spot_ref.get()
    
    if not spot.exists:
        return HttpResponse("Parking spot not found.", status=404)

    # Retrieve the current capacity
    spot_data = spot.to_dict()
    current_capacity = int(spot_data.get("capacity", 0))

    ticket_id = str(uuid4())
    parking_user = ParkingUser.objects.get(id=user_id)
    car_number = parking_user.car_number

    # Check if there's availability
    if current_capacity > 0:
        # Decrease the count by 1
        new_capacity = current_capacity - 1
        spot_ref.update({"capacity": new_capacity,
                         "tickets": firestore.ArrayUnion([ticket_id])})
        
        # Redirect to a confirmation page or back to the details
        return redirect(f"/booking_success/?ticket_id={ticket_id}&car_number={car_number}&spot_id={spot_id}")
    else:
        return HttpResponse("No spots available.", status=400)


@custom_login_required
def home(request):
    return render(request, 'accounts/home.html')