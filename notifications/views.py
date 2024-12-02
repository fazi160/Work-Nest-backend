from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import viewsets, status
from .models import AdminNotificationCreate
from .serializers import AdminNotificationSerializer
from rest_framework.pagination import PageNumberPagination
from space.serializer import ConferenceHallSerializer, CoWorkSpaceSerializer
from space.models import ConferenceHall, CoWorkSpace
from core_auth.serializers import UserSerializer
from core_auth.models import User



class NotificationViewSet(viewsets.ModelViewSet):

    serializer_class = AdminNotificationSerializer

    def get_queryset(self):

        pagination_class = PageNumberPagination

        pagination_class.page_size = 20

        return AdminNotificationCreate.objects.all()


class NotificationDetailView(APIView):
    def get(self, request, type, id, *args, **kwargs):
        try:
            # Print the values to the console (you can replace this with your actual backend logic)
            print(f'Type String: {type}')
            print(f'Identifier: {id}')

            # Initialize serializer and queryset
            serializer = None
            queryset = None

            if type == 'conference':
                serializer = ConferenceHallSerializer
                queryset = ConferenceHall.objects.get(id=id)
            elif type in ['cowork', 'cospace']:
                serializer = CoWorkSpaceSerializer
                queryset = CoWorkSpace.objects.get(id=id)
            elif type in ['user', 'register']:
                serializer = UserSerializer
                queryset = User.objects.get(id=id)
            else:
                return Response({'error': 'Invalid type provided.'}, status=status.HTTP_400_BAD_REQUEST)

            serialized_data = serializer(queryset).data

            return Response({'data': serialized_data, 'message': 'Backend function executed successfully.'}, status=status.HTTP_200_OK)

        except ConferenceHall.DoesNotExist:
            try:
                AdminNotificationCreate.objects.get(
                    notification_type='conference', key=id).delete()
            except AdminNotificationCreate.DoesNotExist:
                pass  # Notification not found, no action needed
            return Response({'error': 'ConferenceHall not found.'}, status=status.HTTP_404_NOT_FOUND)

        except CoWorkSpace.DoesNotExist:
            try:
                AdminNotificationCreate.objects.get(
                    notification_type='cospace', key=id).delete()
            except AdminNotificationCreate.DoesNotExist:
                pass  # Notification not found, no action needed
            return Response({'error': 'CoWorkSpace not found.'}, status=status.HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            try:
                AdminNotificationCreate.objects.get(
                    notification_type='register', key=id).delete()
            except AdminNotificationCreate.DoesNotExist:
                pass  # Notification not found, no action needed
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Handle any exceptions that might occur during execution
            return Response({'error': f'Something went wrong: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BlockUnblockView(APIView):
    def patch(self, request, type, id, *args, **kwargs):
        print(type, id, "data are getting")
        try:
            # Validate 'type'
            if type not in ['cowork', 'conference', 'user', 'register']:
                return Response({'error': 'Invalid type provided.'}, status=status.HTTP_400_BAD_REQUEST)

            # Get the instance based on type
            instance = None
            if type == 'cowork':
                instance = CoWorkSpace.objects.get(id=id)
            elif type == 'conference':
                instance = ConferenceHall.objects.get(id=id)

            elif type == 'user' or type == 'register':
                instance = User.objects.get(id=id)

            if type in ['cowork', 'conference']:
                instance.is_available = not instance.is_available
            elif type in ['user', 'register']:
                instance.is_active = not instance.is_active

            instance.save()

            return Response({'message': 'Block/Unblock operation successful.'}, status=status.HTTP_200_OK)

        except CoWorkSpace.DoesNotExist:
            return Response({'error': 'CoWorkSpace not found.'}, status=status.HTTP_404_NOT_FOUND)
        except ConferenceHall.DoesNotExist:
            return Response({'error': 'ConferenceHall not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Something went wrong: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
