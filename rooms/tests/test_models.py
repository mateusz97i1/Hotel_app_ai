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

    def test_create_room(self)-> None:

        room = HotelRoom.objects.create(
            building = Building.A,
            room_number = "101",
            description = "Has kettle and iron with A/C",
            price_per_night = "150.00",
            max_guests = RoomCapacity.TWO
        )

        assert room.room_id is not None
        assert isinstance(room.room_id, uuid.UUID)
        assert str(room) == f"Building {room.building} - Room {room.room_number}"


    def test_unique_room_per_building_constraint(self)-> None:

        HotelRoom.objects.create(
            building = Building.A,
            room_number = "101",
            description = "Has kettle and iron with A/C",
            price_per_night = "150.00",
            max_guests = RoomCapacity.TWO
        )

        with pytest.raises(IntegrityError):

            HotelRoom.objects.create(
                        building = Building.A,
                        room_number = "101",
                        description = "Has kettle and iron with A/C",
                        price_per_night = "200.00",
                        max_guests = RoomCapacity.FOUR
                    )


    def test_same_room_diffrent_building_allowed(self)-> None:

        HotelRoom.objects.create(
                    building = Building.A,
                    room_number = "101",
                    description = "Has kettle and iron with A/C",
                    price_per_night = "150.00",
                    max_guests = RoomCapacity.TWO
                )


        room_b = HotelRoom.objects.create(
                    building = Building.B,
                    room_number = "101",
                    description = "Has kettle and iron with A/C",
                    price_per_night = "150.00",
                    max_guests = RoomCapacity.TWO
                )

        assert room_b.pk is not None


@pytest.mark.django_db
class TestHotelGuest:


    def test_create_guest(self)-> None:

        guest = HotelGuest.objects.create(
            first_name = "Donald",
            last_name = "Trump",
            date_of_birth = date(1956,2,14),
            id_passport = "CBA6767",
            country = "USA",
            post_code = "76-767",
            phone ="+32563345129",
            email = "mr_president@gmial.com",
        )

        assert guest.guest_id is not None
        assert isinstance(guest.guest_id, uuid.UUID)
        assert str(guest) == "Donald Trump"


    @pytest.mark.parametrize("bad_phone",["ABC","123","+1234567890123456789"])
    def test_invalid_phone_number_raises_validation_error(self, bad_phone:str )-> None:
        pass