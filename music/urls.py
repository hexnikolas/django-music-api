from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("subscription/", views.subscription),
    path("track/<int:track_id>/listen/", views.listen),
    path("search/", views.search),
]
