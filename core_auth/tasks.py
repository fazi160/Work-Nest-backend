from celery import shared_task
from django.core.mail import send_mail


# celery sample task
# @shared_task()
# def send_mail_sample(email):
#     subject = 'Course Enrollment Successful'
#     message = f'Thank you for enrolling in '
#     from_email = 'your_email@example.com'
#     recipient_list = [email]

#     try:
#         send_mail(subject, message, from_email, recipient_list)
#         print('Email sent successfully.')
#     except Exception as e:
#         print(f'An error occurred while sending the email: {e}') 



