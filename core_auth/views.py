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
from .serializers import UserSerializer, myTokenObtainPairSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

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
            

            # creating verification token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # creating verification url
            verification_url = reverse('verify-user', kwargs={'uidb64': uid, 'token': token}) + f'?context=user'

            # Send the verification email
            subject = 'ArtisanHub | Activate Your Account'
            message = f'Hi {user}, Welocme to ArtisanHub..!!  Click the following link to activate your account: {request.build_absolute_uri(verification_url)}'
            from_email = 'copyc195@gmail.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
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

            # creating verification token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # creating verification url
            verification_url = reverse('verify-user', kwargs={'uidb64': uid, 'token': token}) + f'?context=customer'
            

            # Send the verification email
            subject = 'ArtisanHub | Activate Your Account'
            message = f'Hi {user}, Welocme to ArtisanHub..!!  Click the following link to activate your account: {request.build_absolute_uri(verification_url)}'
            from_email = 'copyc195@gmail.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            print('Serializer errors are:', serializer.errors)
            return Response({'status': 'error', 'msg': serializer.errors})


class GoogleAuthentication(APIView):

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        if not User.objects.filter(email=email,is_google=True).exists():
            serializer = GoogleAuthSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):

                user = serializer.save()
                user.user_type = "user"
                user.is_active = True
                user.is_google = True
                user.set_password(password)
                user.save()
        user = authenticate( email=email, password=password)

        if user is not None:
            token=create_jwt_pair_tokens(user)
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

   
    access_token = str(refresh.access_token) # type: ignore
    refresh_token = str(refresh)

    
    return {
        "access": access_token,
        "refresh": refresh_token,
    }



class UserList(ListCreateAPIView):
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['email', 'username', 'user_type', 'is_active']

    def get_queryset(self):
        # # Check if the logged-in user is an admin
        # is_admin = self.request.user.is_superuser

        # # If the logged-in user is an admin, retrieve all users with 'user' user_type
        # if is_admin:
        #     return User.objects.filter(user_type='user').exclude(is_superuser=True)
        # else:
        #     # If the logged-in user is not an admin, return only their own data
        #     return User.objects.filter(id=self.request.user.id)
        return User.objects.filter(user_type='user').exclude(is_superuser=True)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
    

