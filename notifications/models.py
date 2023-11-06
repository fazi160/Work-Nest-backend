from django.db import models
# from core_auth.models import User

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

    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    key = models.IntegerField(null=True, blank=True)

    # cowork = models.ForeignKey(CoWorkSpace, on_delete=models.SET_NULL, null=True, blank=True)

    
    
    
    def __str__(self):  
        return self.name
    
