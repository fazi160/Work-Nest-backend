from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.filters import SearchFilter
from .models import User
from .serializers import UserSerializer, CustomerSerializer, AdminSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserSerializer

class UserRegister(CreateAPIView):
    serializer_class = UserSerializer

class UserList(ListCreateAPIView):
    queryset = User.objects.filter(user_type='user')
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email', 'username']

class UserDetails(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(user_type='user')
    serializer_class = UserSerializer
    lookup_field = 'id'

class CustomerRegister(CreateAPIView):
    serializer_class = CustomerSerializer

class CustomerList(ListCreateAPIView):
    queryset = User.objects.filter(user_type='customer')
    serializer_class = CustomerSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email', 'username']

class CustomerDetails(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(user_type='customer')
    serializer_class = CustomerSerializer
    lookup_field = 'id'

class AdminRegister(CreateAPIView):
    serializer_class = AdminSerializer

class AdminList(ListCreateAPIView):
    queryset = User.objects.filter(user_type='admin')
    serializer_class = AdminSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email', 'username']

class AdminDetails(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(user_type='admin')
    serializer_class = AdminSerializer
    lookup_field = 'id'
