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
        assert str(room) == f"Building A - Room 101"


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

        guest_invalid = HotelGuest(
            first_name = "Dill",
            last_name = "Doe",
            date_of_birth = date(1956,2,14),
            id_passport = "CBA6767",
            country = "USA",
            post_code = "76-767",
            phone = bad_phone,
            email = "mr_diill@gmial.com",
        )

        with pytest.raises(ValidationError):
            guest_invalid.full_clean()


@pytest.mark.django_db
class TestReservation:

    @pytest.fixture
    def room(self) -> HotelRoom:
        return HotelRoom.objects.create(
                building = Building.A,
                room_number = "101",
                description = "Has kettle and iron with A/C",
                price_per_night = "150.00",
                max_guests = RoomCapacity.TWO
            )
        

    @pytest.fixture
    def guest(self) -> HotelGuest:
        return HotelGuest.objects.create(
            first_name = "Donald",
            last_name = "Trump",
            date_of_birth = date(1956,2,14),
            id_passport = "CBA6767",
            country = "USA",
            post_code = "76-767",
            phone ="+32563345129",
            email = "mr_president@gmial.com",
        )


    def test_create_valid_reservation(self, room: HotelRoom, guest: HotelGuest)-> None:

        reservation = Reservation.objects.create(
            room = room,
            guest = guest,
            number_of_guests =2,
            check_in = date(2026,9,1),
            check_out =date(2026,9,8),
        )

        assert reservation.booking_id is not None
        assert isinstance(reservation.booking_id, uuid.UUID)
        assert str(reservation) == (
            f"Booking {reservation.booking_id}: Building A - Room 101 "
            f"for Donald Trump (2026-09-01 -> 2026-09-08)"
        )
        assert reservation.is_cancelled is False


    def test_check_out_before_check_in_raises(self, room: HotelRoom, guest: HotelGuest) -> None:

        reservation_fail = Reservation(
            room = room,
            guest = guest,
            number_of_guests =2,
            check_in = date(2026,9,2),
            check_out =date(2026,9,1),
        )

        with pytest.raises(ValidationError):
            reservation_fail.full_clean()


    def test_overlapping_reservation_raises(self, room: HotelRoom, guest:HotelGuest) -> None:

        reservation = Reservation.objects.create(
                    room = room,
                    guest = guest,
                    number_of_guests =2,
                    check_in = date.today(),
                    check_out =date.today() + timedelta(days=5),
                )

        overlapping = Reservation(
            room = room,
            guest = guest,
            number_of_guests =2,
            check_in = date.today()+ timedelta(days=1),
            check_out =date.today() + timedelta(days=5),
        )

        with pytest.raises(ValidationError):
            overlapping.full_clean()


    def test_non_overlaping_reservation_allowed(self, room: HotelRoom, guest: HotelGuest) -> None:

        reservation = Reservation.objects.create(
            room = room,
            guest = guest,
            number_of_guests =2,
            check_in = date.today(),
            check_out =date.today() + timedelta(days=5),
        )

        non_overlapping = Reservation(
            room = room,
            guest = guest,
            number_of_guests =2,
            check_in = date.today()+ timedelta(days=5),
            check_out =date.today() + timedelta(days=7),
        )
        #should not raise error here
        non_overlapping.full_clean()
        non_overlapping.save()

        assert non_overlapping.pk is not None


    def test_cancelled_reservation_does_not_block_overlap(self, room: HotelRoom, guest:HotelGuest) -> None:

        reservation = Reservation.objects.create(
            room = room,
            guest = guest,
            number_of_guests =2,
            check_in = date.today(),
            check_out =date.today() + timedelta(days=5),
            is_cancelled = True
        )

        new_reservation = Reservation(
            room = room,
            guest = guest,
            number_of_guests =2,
            check_in = date.today(),
            check_out =date.today() + timedelta(days=5),
        )
        #should not raise error here, existing reservation is cancelled
        new_reservation.full_clean()
        new_reservation.save()

        assert new_reservation.pk is not None