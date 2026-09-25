from django.contrib import admin

from .models import HotelGuest,HotelRoom,Reservation

# Register your models here.
@admin.register(HotelGuest)
class HotelGuestAdmin(admin.ModelAdmin):
    pass


@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    pass


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass