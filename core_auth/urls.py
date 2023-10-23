from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('UserRegister/', UserRegister.as_view(), name='UserRegister'),
    path('customerRegister/', CustomerRegister.as_view(), name='customerRegister'),

    path('googleauth/', GoogleAuthentication.as_view(), name='GoogleAuthentication'),   #google authentication register section

    path('verify/<str:uidb64>/<str:token>/', VerifyUserView.as_view(), name='verify-user'), # email verification link

    path('userlist/', UserList.as_view(), name='userlist'), # user list show
    path('customerlist/', CustomerList.as_view(), name='customerlist'), # user list show

]
