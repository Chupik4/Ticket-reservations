from django.urls import path
<<<<<<< HEAD
from .views import simple_view, movies_view, PostListView, PostdetailView, profile_view
=======
from .views import (
    simple_view,
    movies_view,
    PostListView,
    PostdetailView,
    profile_view,
    booking_view,
)
>>>>>>> 782cb0e (Initial commit)

urlpatterns = [
    path("", simple_view, name="home"),
    path("", PostListView.as_view(), name="task-list"),
    path("<int:pk>/", PostdetailView.as_view(), name="task-detail"),
    path("movies/", movies_view, name="movies"),
    path("profile/", profile_view, name="profile"),
<<<<<<< HEAD
=======
    path("booking/", booking_view, name="booking"),
>>>>>>> 782cb0e (Initial commit)
]
