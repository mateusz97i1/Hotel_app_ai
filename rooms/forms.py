from django import forms
from django.forms import ModelForm

from rooms.models import HotelGuest, Reservation, NumberOfGuest


class HotelGuestForm(ModelForm):
    class Meta:
        model = HotelGuest
        fields = ['first_name','last_name','date_of_birth','id_passport','country','post_code','phone','email']


class HotelReservationForm(ModelForm):
    class Meta:
        model= Reservation
        fields = ["room","number_of_guests","check_in","check_out"]
        widgets = {
            "check_in": forms.DateInput(attrs={"type": "date"}),
            "check_out": forms.DateInput(attrs={"type": "date"}),
        }


class AvaliabilityForm(forms.Form):
    """Checks room avaliability"""
    check_in = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    check_out = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    number_of_guest = forms.TypedChoiceField(choices=NumberOfGuest.choices, initial=NumberOfGuest.ONE)


    def clean(self):
        cleaned= super().clean()

        check_in = cleaned.get("check_in")
        check_out = cleaned.get("check_out")

        if check_in > check_out and check_out < check_in :
            raise forms.ValidationError("Check out must be after Check in.")

        return cleaned