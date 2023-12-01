# views.py
from rest_framework import viewsets
from .models import PremiumPackages, PremiumCustomer
from .serializers import PremiumPackagesSerializer, PremiumCustomerSerializer
from django.conf import settings
from rest_framework.views import APIView
import stripe
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core_auth.models import User
from rest_framework.generics import RetrieveAPIView, ListAPIView
from decouple import config
class PremiumPackagesViewSet(viewsets.ModelViewSet):
    queryset = PremiumPackages.objects.all()
    serializer_class = PremiumPackagesSerializer


class PremiumPackagesViewOnly(viewsets.ReadOnlyModelViewSet):
    queryset = PremiumPackages.objects.all()
    serializer_class = PremiumPackagesSerializer



stripe.api_key = 'sk_test_51OFqIQSJiD5G4hPsOp9WDdHeFzGx7va82AmGoZfCXQWfdZILiQgIRY87lYDMQxiy4UoPzb79c7LopwQgNW6aNFdH00cGrA0FV7'
class StripePayment(APIView):
    def post(self, request):
        try:
            data = request.data
            # print(data, "fdasssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")  # This will print the data received in the request
            userId = data.get('userId')
            planId = data.get('planId')
            # You can use the received data to customize the Stripe session creation
            success_url = f'http://localhost:5173/customer/payment/success/?userId={userId}&planId={planId}'
            cancel_url = 'http://localhost:5173/payment/canceled=true'
            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': data.get('currency', 'INR'),
                        'product_data': {
                            'name': data.get('name', 'sample'),
                        },
                        'unit_amount': data.get('unit_amount', 100 * 100),
                    },
                    'quantity': data.get('quantity', 1),
                }],
                mode=data.get('mode', 'payment'),
                success_url=success_url,
                cancel_url=cancel_url,
            )

            print(session)

            return Response({"message": session}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentSuccess(APIView):
    def post(self, request):
        userid = self.request.data.get('userId')
        planid = self.request.data.get('planId')
        print(planid, userid)
        if not userid or not planid:
            return Response({"error": "userId and planId are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            package = PremiumPackages.objects.get(pk=planid)
        except PremiumPackages.DoesNotExist:
            return Response({"error": "Invalid planId"}, status=status.HTTP_400_BAD_REQUEST)

        # Use filter instead of get to handle multiple objects
        premium_customers = PremiumCustomer.objects.filter(user_id=userid)

        if premium_customers.exists():
            # Multiple objects found, handle accordingly
            return Response({"error": "Multiple PremiumCustomer objects found for user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif premium_customers.exists():
            # Single object found, update it
            premium_customer = premium_customers.first()
            premium_customer.package = package
            premium_customer.is_active = True
            premium_customer.save()
        else:
            # No object found, create a new one
            premium_customer = PremiumCustomer.objects.create(user_id=userid, package=package)

        return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)


class PremiumSalesReport(ListAPIView):
    queryset = PremiumCustomer.objects.all()
    serializer_class = PremiumCustomerSerializer
