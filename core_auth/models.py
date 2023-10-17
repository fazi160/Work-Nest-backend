from django.db import models
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
    is_active = models.BooleanField(default=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='user')
    is_google = models.BooleanField(default=False)
    # is_approved = models.BooleanField(default=False)        #to check wether the customer got approved from user or not add this after creating the admin section and notification system



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
