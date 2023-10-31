from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()

# for customer
router.register(r'conference-halls/(?P<customer_id>\d+)', ConferenceHallViewSet, basename='conferencehall')
router.register(r'cowork-spaces/(?P<customer_id>\d+)', CoWorkSpaceViewSet, basename='coworkspace')


# for user
router.register(r'conference', UserConferenceHall, basename='userConference')
router.register(r'cowork',UserCoWorkView, basename='userCoWork')


urlpatterns = [
    path('', include(router.urls)),
]




