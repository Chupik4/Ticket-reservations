from django.shortcuts import render
from django.views.generic import ListView, DetailView
<<<<<<< HEAD
from .models import Contact
=======
from .models import Contact, Booking
>>>>>>> 782cb0e (Initial commit)


class PostListView(ListView):
    model = Contact
    template_name = "home.html"
    context_object_name = "contacts"


class PostdetailView(DetailView):
    model = Contact
    template_name = "home.html"
    context_object_name = "contact"


def movies_view(request):
    return render(request, "movies.html")


def profile_view(request):
<<<<<<< HEAD
    return render(request, "profile.html")
=======
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
    bookings = Booking.objects.all()
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
    name = request.session.get("profile_name", "Users")
    email = request.session.get("profile_email", "user@example.com")
    bookings = Booking.objects.all()
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
        },
    )
>>>>>>> 782cb0e (Initial commit)


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
        contacts = Contact.objects.filter(subject__icontains=search_query)
        return render(request, "home.html", {"contacts": contacts})
    return render(request, "home.html")
<<<<<<< HEAD
=======


def booking_view(request):
    bookings = Booking.objects.all()
    count = bookings.count()
    if count > 0:
        history = f"Історія: {count} бронювань"
    else:
        history = None
    if request.method == "POST":
        movie = request.POST.get("movie")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        date = request.POST.get("date")
        time = request.POST.get("time")
        seats = request.POST.get("seats")
        Booking.objects.create(
            movie=movie,
            first_name=first_name,
            last_name=last_name,
            email=email,
            date=date,
            time=time,
            seats=seats,
        )
        # Update history after creating
        bookings = Booking.objects.all()
        count = bookings.count()
        if count > 0:
            history = f"Історія: {count} бронювань"
        else:
            history = None
        return render(
            request,
            "booking.html",
            {"history": history, "msg": "Бронювання створено успішно!"},
        )
    return render(request, "booking.html", {"history": history})
>>>>>>> 782cb0e (Initial commit)
