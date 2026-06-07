from django.db import IntegrityError, transaction
from django.shortcuts import render

from .models import Booking, BookingSeat, Contact


DEFAULT_MOVIE = "Дуже страшне кіно"
DEFAULT_CINEMA = "Одеса, ТРЦ Gagarinn Plaza"
DEFAULT_HALL = "3"
DEFAULT_DATE = "2026-06-03"
DEFAULT_TIME = "18:40"
DEFAULT_TIME_RANGE = "18:40 - 20:15"

MOVIE_RATINGS = {
    "Дуже страшне кіно": "18+",
    "Нічний рейс": "16+",
    "Місто світла": "12+",
    "Космічна пригода": "6+",
}


def profile_view(request):
    contact_msg = None

    if request.method == "POST":

        if "name" in request.POST:
            name = request.POST.get("name")
            email = request.POST.get("email")

            request.session["profile_name"] = name
            request.session["profile_email"] = email

        elif "cancel_id" in request.POST:
            booking_id = request.POST.get("cancel_id")
            Booking.objects.filter(id=booking_id).delete()

        elif "subject" in request.POST:
            subject = request.POST.get("subject")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            description = request.POST.get("description")

            Contact.objects.create(
                subject=subject,
                first_name=first_name,
                last_name=last_name,
                email=email,
                description=description,
            )

            contact_msg = "Успішно відправлено! Очікуйте відповіді на пошті."

    name = request.session.get("profile_name", "Users")
    email = request.session.get("profile_email", "user@example.com")

    bookings = Booking.objects.prefetch_related("seat_records").all()

    count = bookings.count()
    history = f"{count} бронювань"

    return render(
        request,
        "profile.html",
        {
            "active_bookings": count,
            "history": history,
            "bookings": bookings,
            "profile_name": name,
            "profile_email": email,
            "contact_msg": contact_msg,
        },
    )

def simple_view(request):
    if request.method == "POST":
        subject = request.POST.get("subject")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        description = request.POST.get("description")

        Contact.objects.create(
            subject=subject,
            first_name=first_name,
            last_name=last_name,
            email=email,
            description=description,
        )

    elif request.method == "GET" and "search" in request.GET:
        search_query = request.GET.get("search")

        contacts = Contact.objects.filter(
            subject__icontains=search_query
        )

        return render(
            request,
            "home.html",
            {"contacts": contacts},
        )

    return render(request, "home.html")

def booking_view(request):
    movie = request.GET.get("movie") or DEFAULT_MOVIE

    cinema = DEFAULT_CINEMA
    hall = DEFAULT_HALL
    date = DEFAULT_DATE
    time = DEFAULT_TIME

    if request.method == "POST":
        movie = request.POST.get("movie") or movie
        cinema = request.POST.get("cinema") or cinema
        hall = request.POST.get("hall") or hall
        date = request.POST.get("date") or date
        time = request.POST.get("time") or time

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        selected_list = parse_selected_seats(
            request.POST.get("selected_seats", "")
        )

        occupied_seats = get_occupied_seats(
            movie,
            cinema,
            hall,
            date,
            time,
        )

        if not selected_list:
            return render(
                request,
                "booking.html",
                get_booking_context(
                    movie,
                    cinema,
                    hall,
                    date,
                    time,
                    occupied_seats,
                    error="Оберіть хоча б одне місце.",
                ),
            )

        if set(occupied_seats).intersection(selected_list):
            return render(
                request,
                "booking.html",
                get_booking_context(
                    movie,
                    cinema,
                    hall,
                    date,
                    time,
                    occupied_seats,
                    error="Одне з місць вже зайняте.",
                ),
            )

        try:
            with transaction.atomic():
                total_price = sum(
                    get_seat_price(seat)
                    for seat in selected_list
                )

                booking = Booking.objects.create(
                    movie=movie,
                    cinema=cinema,
                    hall=hall,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    date=date,
                    time=time,
                    seats=len(selected_list),
                    selected_seats=", ".join(selected_list),
                    total_price=total_price,
                )

                BookingSeat.objects.bulk_create(
                    [
                        BookingSeat(
                            booking=booking,
                            movie=movie,
                            cinema=cinema,
                            hall=hall,
                            date=date,
                            time=time,
                            seat_code=seat,
                            seat_type=get_seat_type(seat),
                            price=get_seat_price(seat),
                        )
                        for seat in selected_list
                    ]
                )

        except IntegrityError:
            return render(
                request,
                "booking.html",
                get_booking_context(
                    movie,
                    cinema,
                    hall,
                    date,
                    time,
                    get_occupied_seats(
                        movie,
                        cinema,
                        hall,
                        date,
                        time,
                    ),
                    error="Місце вже заброньоване.",
                ),
            )

        return render(
            request,
            "booking.html",
            get_booking_context(
                movie,
                cinema,
                hall,
                date,
                time,
                get_occupied_seats(
                    movie,
                    cinema,
                    hall,
                    date,
                    time,
                ),
                msg="Бронювання успішне.",
            ),
        )

    return render(
        request,
        "booking.html",
        get_booking_context(
            movie,
            cinema,
            hall,
            date,
            time,
            get_occupied_seats(
                movie,
                cinema,
                hall,
                date,
                time,
            ),
        ),
    )


def parse_selected_seats(raw_seats):
    return [
        seat.strip().upper()
        for seat in raw_seats.split(",")
        if seat.strip()
    ]


def get_seat_type(seat_code):
    return "SUPER LUX" if seat_code.startswith("L") else "GOOD"


def get_seat_price(seat_code):
    return 330 if seat_code.startswith("L") else 210


def get_occupied_seats(movie, cinema, hall, date, time):
    return list(
        BookingSeat.objects.filter(
            movie=movie,
            cinema=cinema,
            hall=hall,
            date=date,
            time=time,
        ).values_list("seat_code", flat=True)
    )


def get_booking_context(
    movie,
    cinema,
    hall,
    date,
    time,
    occupied_seats,
    msg=None,
    error=None,
):
    booking_count = Booking.objects.filter(
        movie=movie,
        cinema=cinema,
        hall=hall,
        date=date,
        time=time,
    ).count()

    history = (
        f"Заброньовано місць: {len(occupied_seats)}"
        if occupied_seats
        else None
    )

    rating = MOVIE_RATINGS.get(movie, "0+")

    return {
        "movie": movie,
        "cinema": cinema,
        "hall": hall,
        "date": date,
        "time": time,
        "time_range": DEFAULT_TIME_RANGE,
        "rating": rating,
        "booking_count": booking_count,
        "history": history,
        "occupied_seats": occupied_seats,
        "msg": msg,
        "error": error,
    }