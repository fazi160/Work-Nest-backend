from django.urls import path
from .views import *
urlpatterns = [
    # admin dashboard urls 'localport/dashboard'
    path('admin/usercount/<str:type>/', UserCountAPIView.as_view(), name='user_count_viewer'),
    path('admin/premium/', TotalRevenueAPI.as_view(), name='total_premium_sales'),
    path('admin/conference/', ConferenceHallSales.as_view(), name='ConferenceHallSales'),
    path('admin/cowork/', CoworkingSpaceSales.as_view(), name='CoworkingSpaceSales'),
    path('admin/premiumplan/', PremiumSales.as_view(), name='PremiumSales'),

    # customer dashboard urls
    path('customer/counts/<int:pk>/',CustomerRelatedCounts.as_view(), name='customer_counts'),
    path('customer/conference/<int:pk>/', ConferenceHallSales.as_view(), name='ConferenceHallSalesCustomer'),
    path('customer/cowork/<int:pk>/', CoworkingSpaceSales.as_view(), name='CoworkingSpaceSalesCustomer')

]
