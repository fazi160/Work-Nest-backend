# views.py
from rest_framework import viewsets
from .models import *
from .serializer import CoWorkBookingDateSerializer, ConferenceBookingDateSerializer, ConferenceHallSerialzer
from rest_framework.pagination import PageNumberPagination
class CoWorkBookingViewSet(viewsets.ModelViewSet):
    queryset = CoWorkBookingDate.objects.all()
    serializer_class = CoWorkBookingDateSerializer

class ConferenceBookingViewSet(viewsets.ModelViewSet):
    queryset = ConferenceBookingDate.objects.all()
    serializer_class = ConferenceBookingDateSerializer
class CoferenceHallViewset(viewsets.ModelViewSet):
    queryset = ConferenceHall.objects.all()
    serializer_class= ConferenceHallSerialzer

    pagination_class = PageNumberPagination
    pagination_class.page_size = 10


