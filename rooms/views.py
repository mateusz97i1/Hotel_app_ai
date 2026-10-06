import logging

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe


from rooms.forms import HotelReservationForm, HotelGuestForm


logger = logging.getLogger(__name__)



@require_safe
def home(request: HttpRequest) -> HttpResponse:
    """simple home page"""
    return render(request, 'home.html')


def book_room(request: HttpRequest) -> HttpResponse:
    """check room avaliability in db"""

    reservation_form = HotelReservationForm()

    return render(request,'book_room.html',context={'reservation_form':reservation_form})