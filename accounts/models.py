from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import random
from django.utils import timezone
from datetime import timedelta
from .tasks import send_otp_via_email

def generate_otp(self):
        otp = str(random.randint(100000, 999999))
        self.otp_code = otp
        self.save()
        return otp

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    is_verified = models.BooleanField(default=False)
    otp_code =  models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"
    
    
    
    def resend_otp(self):
        now = timezone.now()
        otp_validity = timedelta(minutes=1)

        if not self.otp_code or not self.otp_created_at or (self.otp_created_at + otp_validity < now):
            self.otp_code = generate_otp(self)
            self.otp_created_at = now
            self.save()
    
            send_otp_via_email.delay(self.email, self.username, self.otp_code)
            return {"message": "New OTP has been sent."}
        else:
            return {"message": "Current OTP is still valid."}
    
            
         
              


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    # حقول مشتركة
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    # Job Seeker fields
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    # Recruiter fields
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"