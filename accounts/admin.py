from django.contrib import admin
from .models import ParkingUser

@admin.register(ParkingUser)
class ParkingUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email')