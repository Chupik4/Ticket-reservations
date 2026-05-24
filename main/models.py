from django.db import models


class Contact(models.Model):
    subject = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()


class Booking(models.Model):
    movie = models.CharField(max_length=100)
    cinema = models.CharField(max_length=150, default="Одеса, ТРЦ Gagarinn Plaza")
    hall = models.CharField(max_length=20, default="3")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    seats = models.IntegerField(default=1)
    selected_seats = models.TextField(blank=True)
    total_price = models.PositiveIntegerField(default=0)


class BookingSeat(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="seat_records",
    )
    movie = models.CharField(max_length=100)
    cinema = models.CharField(max_length=150)
    hall = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    seat_code = models.CharField(max_length=10)
    seat_type = models.CharField(max_length=20)
    price = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie", "cinema", "hall", "date", "time", "seat_code"],
                name="unique_booked_seat_per_session",
            )
        ]
