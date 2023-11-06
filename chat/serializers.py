from rest_framework.serializers import ModelSerializer
from .models import Message
from core_auth.models import User
# from company.models import ApplyJobs
from core_auth.serializers import UserSerializer
from rest_framework import serializers


class MessageSerializer(ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email')

    class Meta:
        model = Message
        fields = ['message', 'sender_email']

class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'