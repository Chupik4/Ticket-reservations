from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Contact


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
    return render(request, "profile.html")


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
