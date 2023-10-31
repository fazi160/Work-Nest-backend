from django.shortcuts import render

from rest_framework import viewsets, status

from .models import AdminNotificationCreate

from .serializers import *

from rest_framework.pagination import PageNumberPagination

# Create your views here.

class NotificationViewSet(viewsets.ModelViewSet):

    serializer_class = AdminNotificationSerializer


    def get_queryset(self):

        pagination_class = PageNumberPagination

        pagination_class.page_size = 20

        return AdminNotificationCreate.objects.all()
    

