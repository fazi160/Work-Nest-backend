from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.core.serializers import serialize
from channels.layers import get_channel_layer
from .models import ConferenceHall, CoWorkSpace
from asgiref.sync import async_to_sync

@receiver(post_save, sender=ConferenceHall)
def post_save_conference_hall(sender, instance, created, **kwargs):
    # Trigger a notification when a new conference hall is created
    data = f'new Conference Hall {instance.name} has created by {instance.customer.email}'
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'public_room',
            {
                "type": "send_notification",
                "message": data
            }
        )


@receiver(post_save, sender=CoWorkSpace)
def post_save_co_work_space(sender, instance, created, **kwargs):
    data = f'new Co-Working space {instance.name} has created by {instance.customer.email}'
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'public_room',
            {
                "type": "send_notification",
                "message": data
            }
        )