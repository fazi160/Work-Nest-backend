from .models import ConferenceHall
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .models import *
from .serializer import ConferenceHallSerializer, CoWorkSpaceSerializer, ConferenceHallBookingSerializer, CoworkSpaceBookingSerializer, UserPurchaseReportSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import stripe
from datetime import datetime
from django.shortcuts import get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from decouple import config
from django.db.models import Count, F
from rest_framework.generics import RetrieveAPIView

class ConferenceHallViewSet(viewsets.ModelViewSet):

    serializer_class = ConferenceHallSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        pagination_class = PageNumberPagination
        pagination_class.page_size = 10
        return ConferenceHall.objects.filter(customer=customer_id)



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


class BookConferenceHall(APIView):
    def get(self, request, hall_id):

        queryset = ConferenceHallBooking.objects.filter(hall=hall_id)
        serializer = ConferenceHallBookingSerializer(queryset, many=True)
        return Response(serializer.data)




stripe.api_key = config('STRIPE_SECRET_KEY')


class StripePaymentSpace(APIView):
    def post(self, request):

        try:
            data = request.data
            userId = data.get('userId')
            planId = data.get('planId')
            date = data.get('date')
            spaceType = data.get('spaceType')

            print(data, userId, planId, date, spaceType,"---------------------------------------------=======================")

            # You can use the received data to customize the Stripe session creation
            success_url = f'https://worknest.vercel.app/user/spacedetails/payment/success/?userId={userId}&planId={planId}&date={date}&type={spaceType}'

            cancel_url = 'https://worknest.vercel.app/user/spacedetails/payment/canceled'
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
            print("-----------------------------------------------------------------------------------------------------------------------")
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
            booking = ConferenceHallBooking(
                user_id=user_id, hall=hall, booking_date=formatted_date)
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


class CoworkSpaceBookingDataView(APIView):
    def get(self, request, space_id):
        # Aggregate the number of bookings for each date
        unique_dates = CoworkSpaceBooking.objects.filter(space=space_id).values('booking_date', 'space__slots').annotate(total_bookings=Count('booking_date'))

        # Create a list of dictionaries with date and left_space
        response_data = [{'date': entry['booking_date'], 'left_space': entry['space__slots'] - entry['total_bookings']} for entry in unique_dates]

        return Response(response_data)



class CoWorkingSpaceBookingView(APIView):
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

            # Retrieve the coworking space based on the plan_id
            space = get_object_or_404(CoWorkSpace, id=plan_id)

            # Check if available slots for the given space and date are greater than 0
            total_bookings_in_a_day = CoworkSpaceBooking.objects.filter(
                space=space,
                booking_date=formatted_date
            ).count()

            available_slots = space.slots - total_bookings_in_a_day

            if available_slots > 0:
                # If available slots are greater than 0, create a new booking
                booking = CoworkSpaceBooking(
                    user_id=user_id, space=space, booking_date=formatted_date)
                booking.save()
                return Response({"message": "Success"}, status=status.HTTP_201_CREATED)
            else:
                # If available slots are 0 or less, return an error message
                return Response({"error": "No available slots for the given date and space"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CoworkingSpaceSalesReport(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response({"error": "user_id is required in the query parameters."}, status=400)
        
        queryset = CoworkSpaceBooking.objects.filter(space__customer=user_id)
        serializer = CoworkSpaceBookingSerializer(queryset, many=True)
        return Response(serializer.data)


class UserPurchaseReport(RetrieveAPIView):
    serializer_class = UserPurchaseReportSerializer

    def get_object(self):
        user_id = self.kwargs['pk']
        conference_hall_bookings = ConferenceHallBooking.objects.filter(user=user_id)
        cowork_space_bookings = CoworkSpaceBooking.objects.filter(user=user_id)

        data = {
            'conference_hall_bookings': conference_hall_bookings,
            'cowork_space_bookings': cowork_space_bookings,
        }

        return data
    