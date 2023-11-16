from django.db import models
from core_auth.models import User
from notifications.models import AdminNotificationCreate
# Create your models here.
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone

class ConferenceHall(models.Model):

    customer = models.ForeignKey(User,  on_delete=models.CASCADE)

    name = models.CharField(max_length=50)

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
            print('its workkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk', self.id)
            # Create a notification when a new ConferenceHall is created
            notification = AdminNotificationCreate(
                name=f"New Conference Hall Created: {self.name}",
                description=f"A new Conference Hall named '{self.name}' has been created by {self.customer.email}.",
                is_opened=False,
                notification_type='conference',
                key=self.id
            )
            notification.save()

            # Send a notification event
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notifications",  # Channel name for notifications
                {
                    "type": "send.notification",
                    "message": f"New notification: {notification.name}",
                },
            )


    def __str__(self):

        return self.name

    # def is_date_available(self, date):

    #     bookings = ConferenceBooking.objects.filter(

    #         space=self,

    #         start_date__lte=date,
    #         end_date__gte=date
    #     )

    #     return not bool(bookings)

class CoWorkSpace(models.Model):

    customer = models.ForeignKey(User,  on_delete=models.CASCADE)

    name = models.CharField(max_length=50)

    price = models.PositiveIntegerField()

    slots = models.PositiveIntegerField()

    description = models.CharField(max_length=250)

    image = models.ImageField(upload_to='images/space/hall')

    is_available = models.BooleanField(default=False)

    location = models.TextField()

    created_at = models.DateTimeField(auto_now_add=False, default=timezone.now)



    def is_date_available(self, date):

        bookings = CoWorkBooking.objects.filter(

            space=self,

            start_date__lte=date,
            end_date__gte=date
        )

        return not bool(bookings)

    def save(self, *args, **kwargs):
        created = not self.pk  # Check if this is a new instance being created
        super(CoWorkSpace, self).save(*args, **kwargs)

        if created:
            # Create a notification when a new CoWorkSpace is created
            notification = AdminNotificationCreate(
                name=f"New CoWorkSpace Created: {self.name}",
                description=f"A new CoWorkSpace named '{self.name}' has been created by {self.customer.email}.",
                is_opened=False,
                notification_type='cospace',
                cowork=self.pk
            )
            notification.save()

    def __str__(self):

        return self.name


class CoWorkBookingDate(models.Model):

    space = models.ForeignKey(CoWorkSpace, on_delete=models.CASCADE)

    start_date = models.DateField()

    end_date = models.DateField()

    def __str__(self):

        return f"Booking for {self.space} by {self.customer}"


class ConferenceBookingDate(models.Model):

    space = models.ForeignKey(ConferenceHall, on_delete=models.CASCADE)

    start_date = models.DateField()

    end_date = models.DateField()

    def __str__(self):

        return f"Booking for {self.space} by {self.customer}"
