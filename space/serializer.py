# serializers.py
from rest_framework import serializers
from .models import CoWorkBookingDate, ConferenceBookingDate, ConferenceHall, CoWorkSpace

class CoWorkBookingDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoWorkBookingDate
        fields = '__all__'

class ConferenceBookingDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConferenceBookingDate
        fields = '__all__'


class ConferenceHallSerialzer(serializers.ModelSerializer):
    class Meta:
        model = ConferenceHall
        fields = '__all__'