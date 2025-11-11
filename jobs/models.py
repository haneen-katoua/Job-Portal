from django.db import models
from accounts.models import User
from django.conf import settings


class Job(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class SavedJob(models.Model):
    job_seeker = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE,related_name="saved_jobs") 
    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name="saved_by_users")  
    saved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('job_seeker','job') 
   
    def __str__(self):
        return f"{self.job_seeker.username} saved {self.job.title}"    



class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="notification")
    title = models.CharField(max_length=225)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"    
    