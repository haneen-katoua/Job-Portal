from django.core.mail import send_mail
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


@shared_task
def send_otp_via_email(user_email, username, otp):
    subject = "Your OTP Verification Code 🔐"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user_email]

    text_content = f"Hello {username},\nYour OTP code is: {otp}\nThank you for registering!"

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color:#f7f7f7; padding:20px;">
        <div style="max-width:600px; margin:auto; background-color:white; padding:20px; border-radius:10px; text-align:center;">
          <h2 style="color:#333;">Hello {username},</h2>
          <p style="font-size:16px;">Thank you for registering on Job Portal.</p>
          <p style="font-size:18px; font-weight:bold;">Your verification code is:</p>
          <div style="font-size:24px; font-weight:bold; color:#ffffff; background-color:#4CAF50; padding:10px 20px; border-radius:5px; display:inline-block; margin:10px 0;">
            {otp}
          </div>
          <p style="font-size:14px; color:#555;">Please enter this code to verify your account.</p>
        </div>
      </body>
    </html>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()