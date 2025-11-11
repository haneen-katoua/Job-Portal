from rest_framework import serializers
from .models import Job , SavedJob

class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="recruiter.profile.company_name", read_only=True)
    company_location = serializers.CharField(source="recruiter.profile.address", read_only=True)

    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ("recruiter", "created_at", "company_name", "company_location")

class SavedJobSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source= "job.title",read_only=True)
    company_name= serializers.CharField(source="job.recruiter.profile.company_name",read_only=True)
    
    class Meta:
        model = SavedJob
        fields = ['id','job','job_title','company_name','saved_at']
        read_only_fields = ['saved_at']
