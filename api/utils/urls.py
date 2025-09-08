from django.urls import path
from .views import get_coin_price

urlpatterns = [
    path("coin-price/", get_coin_price, name="coin-price"),
]