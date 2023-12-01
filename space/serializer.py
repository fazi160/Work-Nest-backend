# serializers.py
from rest_framework import serializers
from .models import ConferenceHall, CoWorkSpace, ConferenceHallBooking
from core_auth.serializers import UserListSerializer
# class CoWorkBookingDateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CoWorkBookingDate
#         fields = '__all__'

# class ConferenceBookingDateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ConferenceBookingDate
#         fields = '__all__'


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



# class BookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = '__all__'

# serializers.py
from rest_framework import serializers

class ConferenceHallBookingSerializer(serializers.ModelSerializer):
    user_detail = UserListSerializer(source='user', read_only=True)
    hall_detail = ConferenceHallSerializer(source='hall', read_only=True)  
    class Meta:
        model = ConferenceHallBooking
        fields = '__all__'


