import logging

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe, require_GET
from django.db.models import Exists, OuterRef


from rooms.forms import HotelReservationForm, HotelGuestForm, AvailabilityForm

from rooms.models import Reservation, HotelRoom


logger = logging.getLogger(__name__)



@require_safe
def home(request: HttpRequest) -> HttpResponse:
    """simple home page"""
    return render(request, 'home.html')


@require_GET
def check_room_availability(request: HttpRequest) -> HttpResponse:
    """check room availability in db"""

    form = AvailabilityForm(request.GET or None)
    rooms = None

    if form.is_valid():
        check_in_form = form.cleaned_data["check_in"]
        check_out_form = form.cleaned_data["check_out"]
        guests = form.cleaned_data["number_of_guest"]

        busy = Reservation.objects.filter(
            room = OuterRef("pk"),
            is_cancelled = False,
            check_in__lt = check_out_form,
            check_out__gt = check_in_form,
        )

        rooms = HotelRoom.objects.filter(max_guests__gte=guests).filter(~Exists(busy))

    return render(
        request,
        "book_room.html",
        context={"availability_form": form, "available_rooms": rooms},
    )