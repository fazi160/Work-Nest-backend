from rest_framework import serializers
from .models import PremiumPackages

class PremiumPackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumPackages
        fields = '__all__'