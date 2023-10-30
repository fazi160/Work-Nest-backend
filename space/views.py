# views.py
from rest_framework import viewsets, status
from .models import *
from .serializer import CoWorkBookingDateSerializer, ConferenceBookingDateSerializer, ConferenceHallSerializer, CoWorkSpaceSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
class CoWorkBookingViewSet(viewsets.ModelViewSet):
    queryset = CoWorkBookingDate.objects.all()
    serializer_class = CoWorkBookingDateSerializer

class ConferenceBookingViewSet(viewsets.ModelViewSet):
    queryset = ConferenceBookingDate.objects.all()
    serializer_class = ConferenceBookingDateSerializer



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



