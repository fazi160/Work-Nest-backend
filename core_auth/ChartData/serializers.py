from space.models import CoWorkSpace, ConferenceHall, ConferenceHallBooking, ConferenceHallBooking

from rest_framework import serializers


class ConferenceHallAndCoworkSpaceBookingSerializer(serializers.Serializer):
    created_date = serializers.DateField()
    total_sales = serializers.IntegerField()


class PremiumBookingReposrtSerializer(serializers.Serializer):
    package__name = serializers.CharField()
    total_purchase = serializers.IntegerField()
    total_price= serializers.IntegerField()