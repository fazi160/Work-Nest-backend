# serializers.py
from rest_framework import serializers
from .models import CoWorkBooking, ConferenceBooking

class CoWorkBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoWorkBooking
        fields = '__all__'

class ConferenceBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConferenceBooking
        fields = '__all__'
