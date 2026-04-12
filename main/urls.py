from django.urls import path
from .views import simple_view, movies_view, PostListView, PostdetailView, profile_view

urlpatterns = [
    path("", simple_view, name="home"),
    path("", PostListView.as_view(), name="task-list"),
    path("<int:pk>/", PostdetailView.as_view(), name="task-detail"),
    path("movies/", movies_view, name="movies"),
    path("profile/", profile_view, name="profile"),
]
