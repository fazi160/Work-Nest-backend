from django.db import models

class AdminNotificationCreate(models.Model):
    NOTIFICATION_TYPE = (
        ('register', 'register'),
        ('space', 'space'),
    )

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    is_opened = models.BooleanField(default=False)
    notification_type = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPE, default='space')
    
    created_time = models.DateTimeField(auto_now_add=True)

    
    
    def __str__(self):
        return self.name
    
