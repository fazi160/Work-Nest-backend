from django.urls import path
from .views import *
urlpatterns = [

    path("user-previous-chats/<int:user1>/<int:user2>/", PreviousMessagesView.as_view()),
    path('userlist/', UserList.as_view()),
    path('customerlist/', CustomerList.as_view()),
]