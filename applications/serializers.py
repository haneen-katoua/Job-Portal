from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    job_seeker_name = serializers.CharField(source='job_seeker.username', read_only=True)

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ("job_seeker", "status", "created_at")
