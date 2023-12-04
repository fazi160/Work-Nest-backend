from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
import time
from celery import shared_task
from django.contrib.auth import get_user_model
# from space.models import ConferenceHall, CoWorkSpace
class AdminNotificationCreate(models.Model):
    NOTIFICATION_TYPE = (
        ('register', 'register'),
        ('cospace', 'cospace'),
        ('conference', 'conference'),
    )

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    is_opened = models.BooleanField(default=False)
    notification_type = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPE, default='space')
    
    created_time = models.DateTimeField(auto_now_add=True)



    key = models.IntegerField(null=True, blank=True)



    
    
    
    def __str__(self):  
        return self.name
    
# Celery task
@shared_task()
def process_notification(instance_name):
    # Print some text to the console (replace this with your desired action)
    print(f"Notification created: {instance_name}")

@receiver(post_save, sender=AdminNotificationCreate)
def show_text_on_console(sender, instance, created, **kwargs):
    if created:
        # Call the Celery task asynchronously
        process_notification.apply_async(args=[instance.name], countdown=60)



# @receiver(post_save, sender=AdminNotificationCreate)
# def send_webpush_notification(sender, instance, **kwargs):
#     User = get_user_model()

#     # Check if the notification type is one that should trigger a notification
#     if instance.notification_type in ['register', 'cospace', 'conference']:
#         payload = {
#             'head': 'New Notification',
#             'body': f'New {instance.notification_type} notification: {instance.name}',
#         }

#         # Retrieve the user object based on the key (assuming key is the user ID)
#         try:
#             user = User.objects.all()
#             print("Before sending notification")
#             send_user_notification(user=user, payload=payload, ttl=1000)
#             print("After sending notification")
#         except User.DoesNotExist:
#             print(f"User with ID does not exist.")
