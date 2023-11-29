from rest_framework import serializers
from .models import PremiumPackages,PremiumCustomer

class PremiumPackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumPackages
        fields = '__all__'

class PremiumCustomerSerializer(serializers.ModelSerializer):
    package_details = PremiumPackagesSerializer(source='package', read_only=True)

    class Meta:
        model = PremiumCustomer
        fields = '__all__'