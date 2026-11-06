import logging

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe, require_GET
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django_ratelimit.decorators import ratelimit


from rooms.forms import HotelGuestForm, AvailabilityForm, ReservationForm

from rooms.models import Reservation, HotelRoom


logger = logging.getLogger(__name__)



@require_safe
def home(request: HttpRequest) -> HttpResponse:
    """simple home page"""
    return render(request, 'home.html')


@require_GET
@ratelimit(key="ip", rate="100/h", block=True)
def check_room_availability(request: HttpRequest) -> HttpResponse:
    """check room availability in db"""

    form = AvailabilityForm(request.GET or None)
    rooms = None
    qs = ""

    if form.is_bound and form.is_valid(): #bound means that form contains data- not empty
        data = form.cleaned_data
        busy = Reservation.objects.filter(
            room=OuterRef("pk"),
            is_cancelled=False,
            check_in__lt=data["check_out"],
            check_out__gt=data["check_in"],
        )
        rooms = HotelRoom.objects.filter(
            max_guests__gte=data["number_of_guests"]
        ).filter(~Exists(busy))

        #quesrry set for passing data inside url
        check_in = data["check_in"].isoformat()
        check_out = data["check_out"].isoformat()
        guests = data["number_of_guests"]
        qs = f"check_in={check_in}&check_out={check_out}&number_of_guests={guests}"


    context = {
        "availability_form": form,
        "available_rooms": rooms,
        "qs":qs,
    }

    if request.htmx:
        return render(request, "partials/availability_result.html", context)
    return render(request, "check_availability.html", context)


@login_required
def booking_page(request, room_id):

    return render(request,'booking_page.html')


def create_profile_guest(request):

    return render(request,'guest_profile_create.html')