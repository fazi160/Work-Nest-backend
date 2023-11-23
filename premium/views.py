# views.py
from rest_framework import viewsets
from .models import PremiumPackages
from .serializers import PremiumPackagesSerializer

class PremiumPackagesViewSet(viewsets.ModelViewSet):
    queryset = PremiumPackages.objects.all()
    serializer_class = PremiumPackagesSerializer
