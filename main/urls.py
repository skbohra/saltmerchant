from django.urls import path
from . import views



urlpatterns = [
    path("payout/", views.payout, name="payout"),
    path("", views.payout_calculation, name="payout_calculation"),
    path("new_game/", views.new_game, name="new_game"),
    path("add_factory/", views.add_factory, name="add_factory"),
    ]
