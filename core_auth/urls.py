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

    path('userslist/', UserList.as_view(), name='user-list'),

    path('customerlist/', CustomerList.as_view(), name='customer-list'),

    path('usermanagent/<int:pk>/', UserBlock.as_view(), name='user-management'),

    path('customerdetails/', CustomerDetailListCreate.as_view(), name='customer-detail-list-create'),
    path('customerdetails/<int:pk>/', CustomerDetailRetrieveUpdateDestroy.as_view(), name='customer-detail-retrieve-update-destroy'),
    
    path('userdetails/', UserDetailListCreate.as_view(), name='user-detail-list-create'),
    path('userdetails/<int:pk>/', UserDetailRetrieveUpdateDestroy.as_view(), name='user-detail-retrieve-update-destroy'),

    # path('celery/', send_view, name='send view')      # celery sample code url 
]
