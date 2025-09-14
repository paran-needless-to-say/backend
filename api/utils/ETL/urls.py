from django.urls import path
from .views import get_transaction_trace

urlpatterns = [
    path("transaction-trace/", get_transaction_trace, name="transaction-trace"),
]