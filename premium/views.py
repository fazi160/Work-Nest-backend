# views.py
from rest_framework import viewsets
from .models import PremiumPackages
from .serializers import PremiumPackagesSerializer
from django.conf import settings
from rest_framework.views import APIView
import stripe
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status


from decouple import config
class PremiumPackagesViewSet(viewsets.ModelViewSet):
    queryset = PremiumPackages.objects.all()
    serializer_class = PremiumPackagesSerializer


class PremiumPackagesViewOnly(viewsets.ReadOnlyModelViewSet):
    queryset = PremiumPackages.objects.all()
    serializer_class = PremiumPackagesSerializer



stripe.api_key = 'sk_test_51OFqIQSJiD5G4hPsOp9WDdHeFzGx7va82AmGoZfCXQWfdZILiQgIRY87lYDMQxiy4UoPzb79c7LopwQgNW6aNFdH00cGrA0FV7'

class StripePayment(APIView):
    def post(self,request):
        try:
            session = stripe.checkout.Session.create(
            line_items=[{
            'price_data': {
                'currency': 'INR',
                'product_data': {
                'name': 'sample',
                },
                'unit_amount': 100 * 100,
            },
            'quantity': 1 ,
            }],
            mode='payment',
            success_url='http://localhost:5173' + '/success=true',
            cancel_url='http://localhost:5173'  + '/canceled=true',
            
            )
            print(session)

            return Response({ "message" : session },status= status.HTTP_200_OK)
        except Exception as e:

            return Response({ "message" : str(e)},status= status.HTTP_500_INTERNAL_SERVER_ERROR)


