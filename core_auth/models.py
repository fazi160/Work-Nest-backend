from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    USER_TYPES = (
        ('user', 'user'),
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    )

    username = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, unique=True)
    password = models.CharField(max_length=250)
    profile_image = models.ImageField(upload_to='profile', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='user')



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
