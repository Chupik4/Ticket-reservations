from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import (
    simple_view,
    PostListView,
    PostdetailView,
    profile_view,
    booking_view,
)

urlpatterns = [
    path("", simple_view, name="home"),
    path("", PostListView.as_view(), name="task-list"),
    path("<int:pk>/", PostdetailView.as_view(), name="task-detail"),
    path("profile/", profile_view, name="profile"),
    path("booking/", booking_view, name="booking"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
