from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    GenericAPIView,
)
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from verify_email.email_handler import send_verification_email
from .models import User
from .serializers import UserSerializer, myTokenObtainPairSerializer, GoogleAuthSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .models import CustomerDetail, UserDetail
from .serializers import CustomerDetailSerializer, UserDetailSerializer
from rest_framework.pagination import PageNumberPagination
from .tasks import email_verifications

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = myTokenObtainPairSerializer


class UserRegister(CreateAPIView):
    def get_serializer_class(self):
        return UserSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            user.user_type = "user"
            user.set_password(password)
            user.save()
            email_verifications(user,request)
            # # creating verification token
            # token = default_token_generator.make_token(user)
            # uid = urlsafe_base64_encode(force_bytes(user.pk))

            # # creating verification url
            # verification_url = reverse(
            #     'verify-user', kwargs={'uidb64': uid, 'token': token}) + f'?context=user'

            # # Send the verification email
            # subject = 'Work Nest | Activate Your Account'
            # message = f'Hi {user}, Welocme to Work Nest..!!  Click the following link to activate your account: {request.build_absolute_uri(verification_url)}'
            # from_email = 'copyc195@gmail.com'
            # recipient_list = [user.email]
            # send_mail(subject, message, from_email, recipient_list)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('Serializer errors are:', serializer.errors)
            return Response({'status': 'error', 'msg': serializer.errors})


class VerifyUserView(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                context = request.GET.get('context')

                # Create a JWT token for the user
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                # Include the token in the redirect URL query parameter
                if context == 'customer':
                    redirect_url = 'http://localhost:5173/customer/login'
                else:
                    redirect_url = 'http://localhost:5173/user/login'
                return redirect(redirect_url)
            else:
                message = 'Activation Link expired, please register again.'
                redirect_url = 'http://localhost:5173/user/signup'
                return redirect(redirect_url)
        except Exception as e:
            message = 'Activation Link expired, please register again.'
            redirect_url = 'http://localhost:5173/user/signup'
            return redirect(redirect_url)


class CustomerRegister(CreateAPIView):
    def get_serializer_class(self):
        return UserSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            user.user_type = "customer"
            user.set_password(password)
            user.save()
            email_verifications(user,request)


            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            print('Serializer errors are:', serializer.errors)
            return Response({'status': 'error', 'msg': serializer.errors})


class GoogleAuthentication(APIView):

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        if not User.objects.filter(email=email, is_google=True).exists():
            serializer = GoogleAuthSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):

                user = serializer.save()
                user.user_type = "user"
                user.is_active = True
                user.is_google = True
                user.set_password(password)
                user.save()
        user = authenticate(email=email, password=password)

        if user is not None:
            token = create_jwt_pair_tokens(user)
            response_data = {
                'status': 'success',
                'msg': 'Registration Successfully',
                'token': token,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'error', 'msg': serializer.errors})


def create_jwt_pair_tokens(user):

    refresh = RefreshToken.for_user(user)

    refresh['email'] = user.email
    refresh['user_type'] = user.user_type
    refresh['is_active'] = user.is_active
    refresh['is_admin'] = user.is_superuser
    refresh['is_google'] = user.is_google

    access_token = str(refresh.access_token)  # type: ignore
    refresh_token = str(refresh)

    return {
        "access": access_token,
        "refresh": refresh_token,
    }


class UserList(ListCreateAPIView):
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email', 'username', 'user_type', 'is_active']

    # Add PageNumberPagination here
    pagination_class = PageNumberPagination
    # Set the number of items per page as per your requirements
    pagination_class.page_size = 7

    def get_queryset(self):
        # Your existing code to retrieve the queryset
        return User.objects.filter(user_type='user').exclude(is_superuser=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)  # Paginate the queryset
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class UserBlock(APIView):
    def put(self, request, *args, **kwargs):
        # Get the value from the URL parameter
        value_to_update = kwargs.get('pk')
        print(value_to_update)
        if value_to_update is None:
            return Response({'error': 'Please provide a proper input.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the user instance based on the provided pk
            instance = User.objects.get(pk=value_to_update)
            print(instance)
        except User.DoesNotExist:
            return Response({'error': f'User with id={value_to_update} does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Toggle the value of is_active
        instance.is_active = not instance.is_active
        print(instance)
        serializer = UserSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomerList(ListCreateAPIView):
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email', 'username', 'user_type', 'is_active']

    def get_queryset(self):
        return User.objects.filter(user_type='customer')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CustomerDetailListCreate(ListCreateAPIView):
    # print(request.user)
    queryset = CustomerDetail.objects.all()
    serializer_class = CustomerDetailSerializer


class CustomerDetailRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = CustomerDetail.objects.all()
    serializer_class = CustomerDetailSerializer


class UserDetailListCreate(ListCreateAPIView):
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer


class UserDetailRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer





