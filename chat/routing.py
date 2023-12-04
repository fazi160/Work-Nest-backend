
from django.urls import re_path
from django.urls import path
from .consumers import ChatConsumer
from space.consumers import NotificationConsumer
websocket_urlpatterns = [
    path('ws/chat/<int:id>/', ChatConsumer.as_asgi()),
    path('ws/notification/', NotificationConsumer.as_asgi()),
]



