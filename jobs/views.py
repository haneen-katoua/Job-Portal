from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions , filters ,generics
from .models import Job , SavedJob , Notification
from .serializers import JobSerializer , SavedJobSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .utils import create_notification
from accounts.models import User





class JobView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                job = Job.objects.get(pk=pk)
                serializer = JobSerializer(job)
                return Response(serializer.data)
            except Job.DoesNotExist:
                return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            jobs = Job.objects.all()
            search = request.query_params.get("search")
            if search:
                jobs = jobs.filter(
                    Q(title__icontains=search) |
                    Q(description__icontains=search) |
                    Q(location__icontains=search)
                )

            location = request.query_params.get("location")
            if location:
                jobs = jobs.filter(location__iexact=location)

            title = request.query_params.get("title")
            if title:
                jobs = jobs.filter(title__iexact=title)

            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data)

    def post(self, request):
        if request.user.user_type != 'recruiter':
            return Response(
            {"error": "Only recruiters can add jobs"},
            status=status.HTTP_403_FORBIDDEN
        )

    # تحقق من التكرار
        title = request.data.get('title')
        if Job.objects.filter(title=title, recruiter=request.user).exists():
            return Response(
            {"error": "You have already added this job."},
            status=status.HTTP_400_BAD_REQUEST
        )

        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            job = serializer.save(recruiter=request.user)

        # إرسال إشعارات لجميع الباحثين عن عمل
            job_seekers = User.objects.filter(user_type="job_seeker")
            for seeker in job_seekers:
                create_notification(
                user=seeker,
                title="New Job Opportunity 🎯",
                message=f"A new job titled '{job.title}' has been posted. You can apply now!"
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def put(self, request, pk=None):
        if request.user.user_type != "recruiter":
            return Response({"error": "Only recruiters can update jobs"}, status=status.HTTP_403_FORBIDDEN)

        try:
            job = Job.objects.get(pk=pk, recruiter=request.user)
        except Job.DoesNotExist:
            return Response({"error": "Not found or not allowed"}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if request.user.user_type != "recruiter":
            return Response({"error": "Only recruiters can delete jobs"}, status=status.HTTP_403_FORBIDDEN)

        try:
            job = Job.objects.get(pk=pk, recruiter=request.user)
        except Job.DoesNotExist:
            return Response({"error": "Not found or not allowed"}, status=status.HTTP_404_NOT_FOUND)
        job.delete()
        return Response({"message": "Job deleted"}, status=status.HTTP_204_NO_CONTENT)


class SavedJobView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request,job_id):
        user = request.user 
        if user.user_type != "job_seeker":
            return Response({"error":"Only job seekers can save jobs"},status=status.HTTP_403_FORBIDDEN)
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({"error":"job not found"},status=status.HTTP_404_NOT_FOUND)
        saved, created = SavedJob.objects.get_or_create(job_seeker=user,job=job)
        if not created:
            return Response({"message":"Job already saved"},status=status.HTTP_200_OK)
        return Response({"message":"job saved successfully"},status=status.HTTP_201_CREATED)
    
    def get(self,request):
        user = request.user
        if user.user_type != "job_seeker":
            return Response({"error":"Only job seekers can view this."},status=status.HTTP_403_FORBIDDEN)
        saved_jobs = SavedJob.objects.filter(job_seeker=user).order_by('-saved_at')  
        serializer =SavedJobSerializer(saved_jobs,many=True) 
        return Response(serializer.data) 
    
    def delete(self,request,pk):
        user = request.user
        if user.user_type != "job_seeker":
            return Response({"error":"Only job seeker can remove saved job."},status=status.HTTP_403_FORBIDDEN)
        try:
            saved_jobs = SavedJob.objects.get(id=pk,job_seeker=user)
        except SavedJob.DoesNotExist:
            return Response({"error":"saved job not found!"},status=status.HTTP_404_NOT_FOUND)
        saved_jobs.delete()
        return Response({"message":"Job removed from saved list successfully"},status=status.HTTP_204_NO_CONTENT)    
    
    
class NotificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        notification = Notification.objects.filter(user=request.user).order_by('-created_at') 
        data =[
            {
                "id":n.id,
                "title":n.title,
                "message":n.message,
                "is_read":n.is_read,
                "created_at":n.created_at    
            }
            for n in notification
        ]
        return Response(data)
    
    def patch(self,request,pk):
        try:
            notification = Notification.objects.get(pk=pk,user=request.user)
        except Notification.DoesNotExist:
            return Response({"error":"notification not found"},status=status.HTTP_404_NOT_FOUND)
        notification.is_read = True
        notification.save()
        return Response({"message":"notification marked as read"},status=status.HTTP_200_OK)          