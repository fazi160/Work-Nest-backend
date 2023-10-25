# views.py
from rest_framework import viewsets
from .models import CoWorkBooking, ConferenceBooking
from .serializers import CoWorkBookingSerializer, ConferenceBookingSerializer

class CoWorkBookingViewSet(viewsets.ModelViewSet):
    queryset = CoWorkBooking.objects.all()
    serializer_class = CoWorkBookingSerializer

class ConferenceBookingViewSet(viewsets.ModelViewSet):
    queryset = ConferenceBooking.objects.all()
    serializer_class = ConferenceBookingSerializer
