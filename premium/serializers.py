from rest_framework import serializers
from .models import PremiumPackages,PremiumCustomer
from core_auth.serializers import UserListSerializer
class PremiumPackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumPackages
        fields = '__all__'

class PremiumCustomerSerializer(serializers.ModelSerializer):
    package_details = PremiumPackagesSerializer(source='package', read_only=True)
    user_details = UserListSerializer(source='user', read_only=True)

    class Meta:
        model = PremiumCustomer
        fields = '__all__'