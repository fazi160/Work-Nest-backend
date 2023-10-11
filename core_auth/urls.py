from django.urls import path
from .views import UserList, UserDetails, UserRegister, CustomerList, CustomerDetails, CustomerRegister, AdminList, AdminDetails, AdminRegister, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user-list/', UserList.as_view(), name='user_list'),
    path('user-detail/<int:id>/', UserDetails.as_view(), name='user_details'),
    path('user-register/', UserRegister.as_view(), name="user_register"),

    path('customer-list/', CustomerList.as_view(), name='customer_list'),
    path('customer-detail/<int:id>/', CustomerDetails.as_view(), name='customer_details'),
    path('customer-register/', CustomerRegister.as_view(), name="customer_register"),

    path('admin-list/', AdminList.as_view(), name='admin_list'),
    path('admin-detail/<int:id>/', AdminDetails.as_view(), name='admin_details'),
    path('admin-register/', AdminRegister.as_view(), name="admin_register"),
]
