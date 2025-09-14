from django.urls import path
from .views import get_transaction_data

urlpatterns = [
    path("transaction-data/", get_transaction_data, name="transaction-data"),
]