# serializers.py
from rest_framework import serializers
from .models import ConferenceHall, CoWorkSpace, ConferenceHallBooking, CoworkSpaceBooking
from core_auth.serializers import UserListSerializer
from django.db import models

class ConferenceHallSerializer(serializers.ModelSerializer):
    company_data = UserListSerializer(source='customer', read_only=True)

    class Meta:
        model = ConferenceHall
        fields = '__all__'


class CoWorkSpaceSerializer(serializers.ModelSerializer):
    company_data = UserListSerializer(source='customer', read_only=True)

    class Meta:
        model = CoWorkSpace
        fields = '__all__'

class ConferenceHallBookingSerializer(serializers.ModelSerializer):
    user_detail = UserListSerializer(source='user', read_only=True)
    hall_detail = ConferenceHallSerializer(source='hall', read_only=True)

    class Meta:
        model = ConferenceHallBooking
        fields = '__all__'

class CoworkSpaceBookingSerializer(serializers.ModelSerializer):
    left_space = serializers.SerializerMethodField()
    user_detail = UserListSerializer(source='user', read_only=True)
    space_details = CoWorkSpaceSerializer(source='space', read_only=True)
    class Meta:
        model = CoworkSpaceBooking
        fields = '__all__'

    def get_left_space(self, obj):
        total_bookings_in_a_day = CoworkSpaceBooking.objects.filter(
            space=obj.space,
            booking_date=obj.booking_date
        ).count()
        print(obj.space.slots - total_bookings_in_a_day,"left_spaceeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        return obj.space.slots - total_bookings_in_a_day