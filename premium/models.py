# models.py
from django.db import models
from django.utils import timezone
from core_auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from celery import shared_task
from django.dispatch import receiver
from datetime import timedelta

class PremiumPackages(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    validity = models.PositiveIntegerField(default=30)
    description = models.CharField(max_length=250)
    color = models.CharField(max_length=50)

class PremiumCustomer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(PremiumPackages, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)  # Set only when the object is created
    exp_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = timezone.now().date()

        self.exp_date = self.start_date + timedelta(days=self.package.validity)
        super().save(*args, **kwargs)


@receiver(post_save, sender=PremiumCustomer)
def schedule_expiration_task(sender, instance, created, **kwargs):
    if created:
        # Calculate eta based on validity - 1
        eta = instance.package.validity - 1

        # Schedule the expiration reminder task
        expiration_task.apply_async(
            args=[instance.user.email, instance.package.validity],
            countdown=eta * 24 * 60 * 60  # Convert days to seconds
            
        )

@shared_task()
def expiration_task(email, validity):
    # Send an expiration reminder (replace this with your actual message sending logic)
    send_mail(
        'Subscription Expiry Reminder',
        f'Your premium subscription will expire in {validity} days.',
        'from@example.com',
        [email],
        fail_silently=False,
    )
