from django import forms
from django.forms import ModelForm
from django.utils import timezone

from rooms.models import HotelGuest, Reservation, NumberOfGuest


class HotelGuestForm(ModelForm):
    class Meta:
        model = HotelGuest
        fields = ['first_name','last_name','date_of_birth','id_passport','country','post_code','phone','email']


class AvailabilityForm(forms.Form):
    """Checks room avaliability"""
    check_in = forms.DateField(
        initial=timezone.localdate, 
        widget=forms.DateInput(attrs={"type":"date"}, format="%Y-%m-%d")
    )
    check_out = forms.DateField(widget=forms.DateInput(attrs={"type":"date"},format="%Y-%m-%d"))
    number_of_guests = forms.TypedChoiceField(
        choices=NumberOfGuest.choices,
        coerce=int,
        initial=NumberOfGuest.ONE
    )

    def clean_check_in(self):
        """make sure booking reservation in the past is not possible"""
        
        value=self.cleaned_data["check_in"]
        if value < timezone.localdate():
            raise forms.ValidationError("Check in can not be in the past")
        return value

    
    def clean(self):
        cleaned= super().clean()

        check_in = cleaned.get("check_in")
        check_out = cleaned.get("check_out")

        if check_in and check_out and check_out <= check_in:
            raise forms.ValidationError("Check out must be after Check in.")

        return cleaned


class ReservationForm(ModelForm):
    class Meta:
        model= Reservation
        fields = ["room","number_of_guests","check_in","check_out"]
        widgets = {
            "check_in": forms.DateInput(attrs={"type": "date"}),
            "check_out": forms.DateInput(attrs={"type": "date"}),
        }
