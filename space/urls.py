from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register(r'conference-halls/(?P<customer_id>\d+)', ConferenceHallViewSet, basename='conferencehall')
router.register(r'cowork-spaces/(?P<customer_id>\d+)', CoWorkSpaceViewSet, basename='coworkspace')
urlpatterns = [

    path('', include(router.urls)),
]




    # path('conference/', CoferenceHallViewset.as_view({'get': 'list', 'post': 'create'}), name = 'conference'),
    # path('cowork/', CoferenceHallViewset.as_view({'get': 'list', 'post': 'create'}), name = 'cowork'),
    # path('cowork/<int:pk>/', CoferenceHallViewset.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name = 'cowork'),
    # path('conference/<int:pk>/', CoferenceHallViewset.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name = 'conference'),
    # path('cowork-bookings/', CoWorkBookingViewSet.as_view({'get': 'list', 'post': 'create'}), name='cowork-booking-list'),
    # path('cowork-bookings/<int:pk>/', CoWorkBookingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='cowork-booking-detail'),
    # path('conference-bookings/', ConferenceBookingViewSet.as_view({'get': 'list', 'post': 'create'}), name='conference-booking-list'),
    # path('conference-bookings/<int:pk>/', ConferenceBookingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='conference-booking-detail'),

