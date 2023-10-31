from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'admin_notification', NotificationViewSet, basename='admin_notification')

urlpatterns = [
    path('', include(router.urls)),
]
