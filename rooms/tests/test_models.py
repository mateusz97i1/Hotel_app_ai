import pytest
import uuid

from datetime import date, timedelta
from django.urls import reverse
from django.test import Client
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from rooms.models import HotelRoom, HotelGuest, Reservation, Building, RoomCapacity



@pytest.mark.django_db
class TestHotelRoom:

    def test_create_room(self):

        room = HotelRoom.objects.create(
            building = Building.A,
            room_number = "101",
            description = "Has cettle and iron with A/C",
            price_per_night = "150.00",
            max_guests = RoomCapacity.TWO
        )

        assert room.room_id is not None
        assert isinstance(room.room_id, uuid.UUID)
        assert str(room) == f"Building {room.building} - Room {room.room_number}"