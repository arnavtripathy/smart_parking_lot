"""
URL configuration for smart_city_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home, name='home'),
    path('book-spot/<int:spot_id>/', book_spot, name='book_spot'),
    path('confirm-book-spot/<int:spot_id>/', confirm_book_spot, name='confirm_book_spot'),
    path('booking_success/', booking_success, name='booking_success'),
    path('download-ticket/<str:ticket_id>/<str:car_number>/', download_ticket, name='download_ticket'),

]