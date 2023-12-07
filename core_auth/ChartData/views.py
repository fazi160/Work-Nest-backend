from rest_framework.response import Response
from django.http import JsonResponse
from core_auth.models import User
from rest_framework.generics import RetrieveAPIView
from premium.models import PremiumCustomer
from django.db.models import Sum, Count
from space.models import CoworkSpaceBooking, ConferenceHallBooking, CoWorkSpace, ConferenceHall
from .serializers import ConferenceHallAndCoworkSpaceBookingSerializer, PremiumBookingReposrtSerializer

class UserCountAPIView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        user_type_data = kwargs.get('type')
        queryset = User.objects.filter(user_type=user_type_data).count()

        # You should include logic here to serialize the data if needed
        # For simplicity, I'm returning a basic JSON response
        response_data = {'user_count': queryset}

        return JsonResponse(response_data)

class TotalRevenueAPI(RetrieveAPIView):
    def get(self, request, *args, **kwargs):

        total_price = PremiumCustomer.objects.all().aggregate(total_price=Sum('package__price'))
        cowork_revenue = CoworkSpaceBooking.objects.all().aggregate(cowork_revenue=Sum('space__price'))
        conference_revenue = ConferenceHallBooking.objects.all().aggregate(conference_revenue=Sum('hall__price'))
        cowork_count = CoWorkSpace.objects.all().count()
        conference_count=ConferenceHall.objects.all().count()
        response_data = {'data':[total_price,cowork_revenue,conference_revenue,{'cowork_space_count':cowork_count},{'conference_space_count':conference_count}]}
        return JsonResponse(response_data)

class ConferenceHallSales(RetrieveAPIView):
    queryset = ConferenceHallBooking.objects.all()
    serializer_class = ConferenceHallAndCoworkSpaceBookingSerializer

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if user_id:
            sales_data = self.queryset.filter(hall__customer=user_id).values('created_date').annotate(total_sales=Sum('price'))
        else:
            sales_data = self.queryset.values('created_date').annotate(total_sales=Sum('price'))

        # Serialize the data
        serialized_data = self.serializer_class(sales_data, many=True).data

        return JsonResponse(serialized_data, safe=False)

class CoworkingSpaceSales(RetrieveAPIView):
    queryset = CoworkSpaceBooking.objects.all()
    serializer_class = ConferenceHallAndCoworkSpaceBookingSerializer

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if user_id:
            annotated_queryset = self.queryset.filter(space__customer=user_id).values('created_date').annotate(total_sales=Sum('price'))
        # Annotate the queryset to get total sales for each booking date
        else:
            annotated_queryset = self.queryset.values('created_date').annotate(total_sales=Sum('price'))

        # Serialize the annotated queryset
        serialized_data = self.serializer_class(annotated_queryset, many=True).data

        return JsonResponse(serialized_data, safe=False)

class PremiumSales(RetrieveAPIView):
    queryset = PremiumCustomer.objects.all()
    serializer_class = PremiumBookingReposrtSerializer

    def get(self, request, *args, **kwargs):
        # Annotate the queryset with total purchase count and total price
        annotated_queryset = self.queryset.values('package__name').annotate(
            total_purchase=Count('package'),
            total_price=Sum('package__price')
        )

        # Return the annotated data
        return Response(annotated_queryset)




# for customer dashboard
class CustomerRelatedCounts(RetrieveAPIView):
    def get(self, request, *args ,**kwargs):
        user_id = kwargs.get('pk')
        conference_count = ConferenceHall.objects.filter(customer=user_id).count()
        cowork_count = CoWorkSpace.objects.filter(customer=user_id).count()
        cowork_booking_count = CoworkSpaceBooking.objects.filter(space__customer=user_id).count()
        conference_booking_count = ConferenceHallBooking.objects.filter(hall__customer=user_id).count()
        response_data= {"data":[conference_count,cowork_count,cowork_booking_count,conference_booking_count]}
        return JsonResponse(response_data)


