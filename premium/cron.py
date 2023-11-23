# premium/cron.py

from celery import Celery
from celery.schedules import crontab
from .models import PremiumCustomer, Category
from .tasks import send_exp_date_email
import random
# app = Celery('premium')  # Replace 'your_app_name' with your actual app name

@app.task
def exp_time_decrease():
    PremiumCustomer.objects.filter(exp_date__gt=1).update(exp_date=models.F('exp_date') - 1)
    print("cron is workinggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg")
    # Check if exp_date is 1 and send email using Celery task
    expiring_users = PremiumCustomer.objects.filter(exp_date=1)
    for user in expiring_users:
        send_exp_date_email.delay(user.user.email)


    
