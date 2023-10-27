from django.urls import path
from .views import *

urlpatterns = [
    path('conference/', CoferenceHallViewset.as_view({'get': 'list', 'post': 'create'}), name = 'conference'),
    path('conference/<int:pk>/', CoferenceHallViewset.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name = 'conference'),
    path('cowork-bookings/', CoWorkBookingViewSet.as_view({'get': 'list', 'post': 'create'}), name='cowork-booking-list'),
    path('cowork-bookings/<int:pk>/', CoWorkBookingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='cowork-booking-detail'),
    path('conference-bookings/', ConferenceBookingViewSet.as_view({'get': 'list', 'post': 'create'}), name='conference-booking-list'),
    path('conference-bookings/<int:pk>/', ConferenceBookingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='conference-booking-detail'),
]


