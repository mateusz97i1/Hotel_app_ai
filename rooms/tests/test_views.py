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


@pytest.mark.django_db
class TestRoomAvailabilityView:
    """form checks room availability in db"""


    url_name ="rooms:room_availability"
    template_name = "check_availability.html"
    partial_name = "partials/availability_result.html"

    @pytest.fixture
    def params(self) -> dict:
        """quick reservation paremetrs"""

        check_in = date.today() + timedelta(days=1)
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

    
    def test_form_is_valid_render_results(self, client: Client, params :dict) -> None:
        """uses baker for: Automatically generates test data for Django models"""

        hotel_room = baker.make('HotelRoom', max_guests=2)

        url = reverse(self.url_name)

        response = client.get(url,params)

        assert response.status_code == 200
        assert self.partial_name in [t.name for t in response.templates]
        assert list(response.context["available_rooms"]) == [hotel_room]


    def test_busy_room_is_excluded(self, client: Client, params: dict) -> None:

        free = baker.make('HotelRoom', max_guests = 2)
        busy = baker.make('HotelRoom', max_guests = 2)
        guest = baker.make('Reservation',
                        room = busy,
                        check_in = params["check_in"],
                        check_out = params["check_out"],
                        is_cancelled = False,
                        number_of_guests = 2)

        url = reverse(self.url_name)

        response = client.get(url,params)

        assert response.status_code == 200
        assert list(response.context["available_rooms"]) == [free]


    def test_cancelled_resrvation_does_not_block_room(self, client: Client, params: dict) -> None:

        cancelled = baker.make('HotelRoom', max_guests = 2)
        guest = baker.make('Reservation',
                        room = cancelled,
                        check_in = params["check_in"],
                        check_out = params["check_out"],
                        is_cancelled = True,
                        number_of_guests =2 )

        url = reverse(self.url_name)

        response = client.get(url,params)

        assert response.status_code == 200
        assert list(response.context["available_rooms"]) == [cancelled]


    def test_room_is_too_small_excluded(self, client : Client, params : dict) -> None:

        params["number_of_guest"] = 3

        small = baker.make('HotelRoom', max_guests = 2)

        url = reverse(self.url_name)

        response = client.get(url, params)

        assert response.status_code == 200
        assert list(response.context["available_rooms"]) == []


    def test_invalid_form_returns_no_rooms(self, client: Client) -> None:

        url= reverse(self.url_name)

        response = client.get(url,{"check_in": "no-date"})

        assert response.status_code == 200
        assert response.context["available_rooms"] is None
        assert response.context["availability_form"].errors


    def test_htmx_request_renders_partial(self, client: Client, params: dict) -> None:

        url = reverse(self.url_name)
        response = client.get(url,params,headers={"HX-Request":"true"})

        assert self.partial_name in [t.name for t in response.templates]
        assert self.template_name not in [t.name for t in response.templates]