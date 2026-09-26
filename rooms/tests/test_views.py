import pytest

from django.urls import reverse
from django.test import Client

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