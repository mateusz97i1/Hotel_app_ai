import uuid

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db import models


class Building(models.TextChoices):
    A = "A", "Building A"
    B = "B", "Building B"


class RoomCapacity(models.IntegerChoices):
    TWO = 2, "Up to 2 guests"
    FOUR = 4, "Up to 4 guests"


class HotelRoom(models.Model):
    """DB of all existing rooms."""

    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    building = models.CharField(max_length=1, choices=Building.choices)
    room_number = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    max_guests = models.PositiveSmallIntegerField(choices=RoomCapacity.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["building", "room_number"], name="unique_room_per_building"
            )
        ]

    def __str__(self):
        return f"Building {self.building} - Room {self.room_number}"


class HotelGuest(models.Model):
    """Lead guest data needed for making a reservation."""

    phone_validator = RegexValidator(
        regex=r"^\+?\d{7,15}$", message="Enter a valid phone number."
    )

    guest_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    id_passport = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, validators=[phone_validator])
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Reservation(models.Model):
    """A booking linking a guest to a room for a given date range."""

    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(
        HotelRoom, on_delete=models.PROTECT, related_name="reservations"
    )
    guest = models.ForeignKey(
        HotelGuest, on_delete=models.PROTECT, related_name="reservations"
    )
    number_of_guests = models.PositiveSmallIntegerField()
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)



    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(check_out__gt=models.F("check_in")),
                name="check_out_after_check_in",
            )
        ]

    def clean(self):
        if self.check_out <= self.check_in:
            raise ValidationError("Check out must be after Check in.")

        overlapping = Reservation.objects.filter(
            room = self.room,
            is_cancelled = False,
            check_in__lt=self.check_out,
            check_out__gt=self.check_in

        ).exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError("This room is already booked for the selected dates.")


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Booking {self.booking_id}: {self.room} for {self.guest} ({self.check_in} -> {self.check_out})"