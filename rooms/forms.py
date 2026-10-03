from django.forms import ModelForm

from rooms.models import Reservation

class HotelResrvationForm(ModelForm):
    class Meta:
        model= Reservation
        fields = ["room","guest","number_of_guests","check_in","check_out"]