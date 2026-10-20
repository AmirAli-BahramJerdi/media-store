from django.urls import path
from . import views

app_name = "repairs"

urlpatterns = [
    path("api/track/", views.TrackApiView.as_view(), name="track_api"),
]