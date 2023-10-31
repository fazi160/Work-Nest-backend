from rest_framework import serializers


from .models import AdminNotificationCreate


class AdminNotificationSerializer(serializers.ModelSerializer):

    class Meta:

        model = AdminNotificationCreate

        fields = '__all__'