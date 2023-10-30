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


class ConferenceHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConferenceHall
        fields = '__all__'

class CoWorkSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoWorkSpace
        fields = '__all__'