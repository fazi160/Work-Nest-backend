from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile_image', 'user_type']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user_type = validated_data.pop('user_type', 'user')
        instance = self.Meta.model.objects.create(**validated_data, user_type=user_type)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class CustomerSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile_image', 'user_type']
        extra_kwargs = {
            'password': {'write_only': True},
        }

class AdminSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile_image', 'user_type']
        extra_kwargs = {
            'password': {'write_only': True},
        }
