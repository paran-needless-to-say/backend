from django.urls import path
from . import views

urlpatterns = [
    path('next-hops/', views.next_hops, name='next-hops'),
]






