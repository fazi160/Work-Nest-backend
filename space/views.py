# views.py
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .models import *
from .serializer import  ConferenceHallSerializer, CoWorkSpaceSerializer, ConferenceHallBookingSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import stripe
from datetime import datetime
from django.shortcuts import get_object_or_404

# class CoWorkBookingViewSet(viewsets.ModelViewSet):
#     queryset = CoWorkBookingDate.objects.all()
#     serializer_class = CoWorkBookingDateSerializer

# class ConferenceBookingViewSet(viewsets.ModelViewSet):
#     queryset = ConferenceBookingDate.objects.all()
#     serializer_class = ConferenceBookingDateSerializer




# for customer works
class ConferenceHallViewSet(viewsets.ModelViewSet):
    
    serializer_class = ConferenceHallSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        pagination_class = PageNumberPagination
        pagination_class.page_size = 10
        return ConferenceHall.objects.filter(customer=customer_id)


    # def partial_update(*args, **kwargs):
    #     print(request)


class CoWorkSpaceViewSet(viewsets.ModelViewSet):
    
    serializer_class = CoWorkSpaceSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        pagination_class = PageNumberPagination
        pagination_class.page_size = 10
        return CoWorkSpace.objects.filter(customer=customer_id)


# for user

class UserCoWorkView(viewsets.ReadOnlyModelViewSet):
    serializer_class = CoWorkSpaceSerializer
    queryset = CoWorkSpace.objects.filter(is_available=True)

class UserConferenceHall(viewsets.ReadOnlyModelViewSet):
    serializer_class = ConferenceHallSerializer
    queryset = ConferenceHall.objects.filter(is_available=True)


# class BookingViewSet(viewsets.ModelViewSet):
#     queryset = Booking.objects.all()
#     serializer_class = ConferenceHallBookingSerializer

class BookConferenceHall(APIView):
    def get(self, request, hall_id):
       
        queryset = ConferenceHallBooking.objects.filter(hall=hall_id)
        serializer = ConferenceHallBookingSerializer(queryset, many=True)
        return Response(serializer.data) 

    # def post(self, request, hall_id):
    #     hall = ConferenceHall.objects.get(pk=hall_id)
    #     booking_date = request.data.get('booking_date')
    #     user_id = request.data.get('user_id')
        
        
    #     # Check if the date is available
    #     if not ConferenceHallBooking.objects.filter(hall=hall, booking_date=booking_date).exists():
    #         # Create a new booking
    #         booking = ConferenceHallBooking(hall=hall, booking_date=booking_date, user=user_id)
    #         booking.save()
    #         return Response({'message': 'Booking successful'}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({'message': 'The hall is already booked for this date'}, status=status.HTTP_400_BAD_REQUEST)

stripe.api_key = 'sk_test_51OFqIQSJiD5G4hPsOp9WDdHeFzGx7va82AmGoZfCXQWfdZILiQgIRY87lYDMQxiy4UoPzb79c7LopwQgNW6aNFdH00cGrA0FV7'
class StripePaymentSpace(APIView):
    def post(self, request):
        print("the functions is called..........................................................................................")
        try:
            data = request.data
            userId = data.get('userId')
            planId = data.get('planId')
            date = data.get('date')


            print(userId,planId,date,"fdsaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaafdsafdfa")
            
            # You can use the received data to customize the Stripe session creation
            success_url = f'http://localhost:5173/user/spacedetails/payment/success/?userId={userId}&planId={planId}&date={date}'

            cancel_url = 'http://localhost:5173/user/spacedetails/payment/canceled'
            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': data.get('currency', 'INR'),
                        'product_data': {
                            'name': data.get('space_name', 'sample'),
                        },
                        'unit_amount': data.get('price', 100 * 100),
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

class ConferenceHallBookingView(APIView):

    def post(self, request):
    
        try:
            print("try is started")
            user_id = self.request.data.get('userId')
            plan_id = self.request.data.get('planId')
            date_str = self.request.data.get('date')
      
            date_str = str(date_str)
            print(type(date_str))
            # Convert the date string to a datetime object
            date_object = datetime.strptime(date_str, '%d/%m/%Y')
            formatted_date = date_object.date()
            # Check if there is an existing booking for the same plan and date
            existing_booking = ConferenceHallBooking.objects.filter(
                user_id=user_id,
                hall__customer_id=plan_id,
                booking_date=formatted_date
            ).first()

            if existing_booking:
                return Response({"error": "Booking already exists for this date and plan."}, status=status.HTTP_400_BAD_REQUEST)

          

            # Retrieve the conference hall based on the plan_id
            hall = get_object_or_404(ConferenceHall, id=plan_id)

            # Create a new booking
            booking = ConferenceHallBooking(user_id=user_id, hall=hall, booking_date=formatted_date)
            booking.save()

            return Response({"message": "Success"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SpaceSalesReport(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')


        # Check if user_id is provided in the query parameters
        if not user_id:
            return Response({"error": "user_id is required in the query parameters."}, status=400)

        # Query ConferenceHallBooking instances based on the customer's user_id
        queryset = ConferenceHallBooking.objects.filter(hall__customer=user_id)

        # Serialize the queryset before returning it in the response
        serializer = ConferenceHallBookingSerializer(queryset, many=True)
        return Response(serializer.data)


