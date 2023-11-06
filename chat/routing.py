from django.urls import path
from .consumers import ChatConsumer
from notifications.consumers import NotificationConsumer
websocket_urlpatterns = [
    path('ws/chat/<int:id>/', ChatConsumer.as_asgi()),
    path('ws/notification/', NotificationConsumer.as_asgi()),

    
]