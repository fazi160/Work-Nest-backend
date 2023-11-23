from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.urls import reverse

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

@shared_task()
def email_verifications(user,request):
        # creating verification token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # creating verification url
        verification_url = reverse(
            'verify-user', kwargs={'uidb64': uid, 'token': token}) + f'?context=user'

        # Send the verification email
        subject = 'Work Nest | Activate Your Account'
        message = f'Hi {user}, Welocme to Work Nest..!!  Click the following link to activate your account: {request.build_absolute_uri(verification_url)}'
        from_email = 'copyc195@gmail.com'
        recipient_list = [user.email]
        try:
            send_mail(subject, message, from_email, recipient_list)
            print("mail sended successfully")
        except Exception as e:
            print(f'An error occurred while sending the email: {e}')





