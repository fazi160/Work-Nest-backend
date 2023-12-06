from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()

# for customer
router.register(r'conference-halls/(?P<customer_id>\d+)', ConferenceHallViewSet, basename='conferencehall')
router.register(r'cowork-spaces/(?P<customer_id>\d+)', CoWorkSpaceViewSet, basename='coworkspace')

# Booking
# router.register(r'bookings', BookingViewSet, basename='booking')

# for user
router.register(r'conference', UserConferenceHall, basename='userConference')
router.register(r'cowork',UserCoWorkView, basename='userCoWork')


urlpatterns = [
    path('', include(router.urls)),
    path('booking/payment/', StripePaymentSpace.as_view(), name = 'premium_payment'),
    path('conference/<int:hall_id>/book/', BookConferenceHall.as_view(), name='BookConferenceHall'),
    path('cowork/<int:space_id>/book/', CoworkSpaceBookingDataView.as_view(), name='CoworkSpaceBookingViewSet'),
    path('conference/booking/register/', ConferenceHallBookingView.as_view(), name='conference_hall_booking'),
    path('cowork/booking/register/', CoWorkingSpaceBookingView.as_view(), name='co_work_booking'),
    path('hall/salesreport/', SpaceSalesReport.as_view(), name='SpaceSalesReport'),
    path('co-work/salesreport/', CoworkingSpaceSalesReport.as_view(), name='CoWorkSalesReport'),
    path('user/purchase/<int:pk>/', UserPurchaseReport.as_view(), name='UserPurchaseReport')
]




