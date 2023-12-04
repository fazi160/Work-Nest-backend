from django.db import models
from core_auth.models import User
from notifications.models import AdminNotificationCreate
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
# from .consumers import SpaceNotificationConsumer


class ConferenceHall(models.Model):

    customer = models.ForeignKey(User,  on_delete=models.CASCADE)

    name = models.CharField(max_length=150)

    price = models.PositiveIntegerField()

    Capacity = models.PositiveIntegerField()

    description = models.CharField(max_length=250)

    image = models.ImageField(upload_to='images/space/hall')

    is_available = models.BooleanField(default=False)

    location = models.TextField()

    created_at = models.DateTimeField(auto_now_add=False, default=timezone.now)

    def save(self, *args, **kwargs):
        created = not self.pk  # Check if this is a new instance being created
        super(ConferenceHall, self).save(*args, **kwargs)

        if created:
            
            # Create a notification when a new ConferenceHall is created
            notification = AdminNotificationCreate(
                name=f"New Conference Hall Created: {self.name}",
                description=f"A new Conference Hall named '{self.name}' has been created by {self.customer.email}.",
                is_opened=False,
                notification_type='conference',
                key=self.id
            )
            notification.save()

    def __str__(self):

        return self.name


class CoWorkSpace(models.Model):

    customer = models.ForeignKey(User,  on_delete=models.CASCADE)

    name = models.CharField(max_length=150)

    price = models.PositiveIntegerField()

    slots = models.PositiveIntegerField()

    description = models.CharField(max_length=250)

    image = models.ImageField(upload_to='images/space/cowork')

    is_available = models.BooleanField(default=False)

    location = models.TextField()

    created_at = models.DateTimeField(auto_now_add=False, default=timezone.now)

    def save(self, *args, **kwargs):
        created = not self.pk  # Check if this is a new instance being created
        super(CoWorkSpace, self).save(*args, **kwargs)

        if created:
            # Create a notification when a new CoWorkSpace is created
            notification = AdminNotificationCreate(
                name=f"New CoWorkSpace Created: {self.name}",
                description=f"A new Co-Working Space named '{self.name}' has been created by {self.customer.email}.",
                is_opened=False,
                notification_type='cowork',
                key=self.pk
            )
            notification.save()

    def __str__(self):

        return self.name


class ConferenceHallBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hall = models.ForeignKey(ConferenceHall, on_delete=models.CASCADE)
    booking_date = models.DateField()
    price = models.IntegerField(null=True)

    def save(self, *args, **kwargs):

        self.price = self.hall.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.hall.name} - {self.user.email}"






