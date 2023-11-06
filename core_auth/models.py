from django.db import models
from notifications.models import *
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):

    USER_TYPES = (
        ('user', 'user'),

        ('customer', 'Customer'),

        ('admin', 'Admin'),
    )


    username = models.CharField(max_length=250, null=True)

    email = models.EmailField(max_length=250, unique=True)

    password = models.CharField(max_length=250)

    profile_image = models.ImageField(upload_to='images/profile', blank=True, null=True)

    is_active = models.BooleanField(default=False)

    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='user')

    is_google = models.BooleanField(default=False)

    is_approved = models.BooleanField(default=False)        #to check wether the customer got approved from user or not add this after creating the admin section and notification system




    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        created = not self.pk  # Check if this is a new instance being created
        super(User, self).save(*args, **kwargs)

        if created and self.user_type == 'customer':
            # Create a notification when a new CoWorkSpace is created
            notification = AdminNotificationCreate(
                name=f"New User Created: {self.email}",
                description=f"A new Customer created named '{self.name}'",
                is_opened=False,
                notification_type='register',
                # user = self.pk
                
            )
            notification.save()





class CustomerDetail(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    company_name = models.CharField(max_length=50)

    contact = models.CharField()
    
    description = models.TextField(null=True)


class UserDetail(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    occupation = models.CharField(max_length=50)

    contact = models.CharField()

