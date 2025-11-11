from django.db import models
from accounts.models import User
from jobs.models import Job
from django.core.mail import send_mail
from django.conf import settings



class Application(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(blank=True, null=True)
    cv = models.FileField(upload_to='applications_cvs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_seeker.username} applied for {self.job.title}"



    