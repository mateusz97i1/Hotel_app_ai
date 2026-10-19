import pytest

from datetime import date, timedelta
from django.urls import reverse

from django.test import Client
from unittest import mock
from model_bakery import baker


from rooms.models import HotelGuest, HotelRoom, Reservation

# ------------------ FIXTURES---------------

#------------------TEST_CASES--------------

class TestBaseView:
    """"Test base views that only render templates"""

    url_name = 'rooms:home'
    template_name = 'home.html'

    def test_template_renders_correctly(self, client: Client)-> None:

        url = reverse(self.url_name)

        response = client.get(url)

        assert response.status_code == 200
        assert self.template_name in [t.name for t in response.templates]



class TestRoomAvailabilityView:
    """form checks room availability in db"""


    url_name ="rooms:room_availability"
    template_name = "check_availability.html"
    partial_name = "partials/availability_result.html"

    @pytest.fixture
    def params(self) -> dict:
        """quick reservation paremetrs"""

        check_in = date.today()+timedelta(days=10)
        return{
            "check_in" : check_in,
            "check_out" : check_in + timedelta(days=3),
            "number_of_guest" : 2
        }

    

    def test_template_renders_correctly(self, client: Client) -> None:

        url = reverse(self.url_name)

        response = client.get(url)

        assert response.status_code == 200
        assert self.template_name in [t.name for t in response.templates]

    @pytest.mark.django_db
    def test_form_is_valid_render_results(self, client: Client, params :dict) -> None:
        """uses baker for: Automatically generates test data for Django models"""

        hotel_room = baker.make('HotelRoom', max_guests=2)

        url = reverse(self.url_name)

        response = client.get(url,params)

        assert response.status_code == 200
        assert self.partial_name in [t.name for t in response.templates]
        assert list(response.context["available_rooms"]) == [hotel_room]
