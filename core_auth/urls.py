from django.urls import path, include
from .views import *

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'user/details/(?P<user_id>\d+)', UserDetailViewSet, basename='UserDetailViewSet')


urlpatterns = [
    path('',include(router.urls)),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('UserRegister/', UserRegister.as_view(), name='UserRegister'),
    path('customerRegister/', CustomerRegister.as_view(), name='customerRegister'),

    # google authentication register section
    path('googleauth/', GoogleAuthentication.as_view(),
         name='GoogleAuthentication'),

    path('verify/<str:uidb64>/<str:token>/', VerifyUserView.as_view(),
         name='verify-user'),  # email verification link

    path('userslist/', UserList.as_view(), name='user-list'),

    path('customerlist/', CustomerList.as_view(), name='customer-list'),

    path('usermanagent/<int:pk>/', UserBlock.as_view(), name='user-management'),

    path('customerdetails/', CustomerDetailListCreate.as_view(),
         name='customer-detail-list-create'),
    path('customerdetails/<int:pk>/', CustomerDetailRetrieveUpdateDestroy.as_view(),
         name='customer-detail-retrieve-update-destroy'),



    path('userdetail/<int:pk>/', CustomerDetails.as_view(), name='user-detail'),

    # path('user/userdata/create/',
    #      UserDetailsCreate.as_view(), name='user-detail-create'),
    # path('user/userdata/<int:pk>/',
    #      UserDetails.as_view(), name='user-detail'),


]
