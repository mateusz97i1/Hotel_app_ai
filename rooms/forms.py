from django.forms import ModelForm

from rooms.models import HotelGuest, Reservation


class HotelGuestForm(ModelForm):
    class Meta:
        model = HotelGuest
        fields = ['first_name','last_name','date_of_birth','id_passport','country','post_code','phone','email']


class HotelReservationForm(ModelForm):
    class Meta:
        model= Reservation
        fields = ["room","number_of_guests","check_in","check_out"]