from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Application
from .serializers import ApplicationSerializer
from jobs.models import Job
from .tasks import send_status_notification

class ApplicationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.user_type != "job_seeker":
            return Response({"error": "Only job seekers can view this"}, status=403)
        applications = Application.objects.filter(job_seeker=request.user)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    def post(self, request):
        job_id = request.data.get("job")
        if not job_id:
            return Response({"error": "Job ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.user_type != "job_seeker":
            return Response({"error": "Only job seekers can apply"}, status=status.HTTP_403_FORBIDDEN)

        if Application.objects.filter(job=job, job_seeker=request.user).exists():
            return Response({"error": "You have already applied for this job"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(job_seeker=request.user, job=job)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ApplicationsForRecruiterView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.user_type != "recruiter":
            return Response({"error": "Only recruiters can view this"}, status=403)

        applications = Application.objects.filter(job__recruiter=request.user)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)
    
    
    def patch(self, request, pk):
        if request.user.user_type != "recruiter":
            return Response({"error": "Only recruiters can update status"}, status=status.HTTP_403_FORBIDDEN)

        try:
            application = Application.objects.get(pk=pk, job__recruiter=request.user)
        except Application.DoesNotExist:
            return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get("status")
        valid_statuses = ["under_review", "accepted", "rejected"]

        if new_status not in valid_statuses:
            return Response({"error": "Invalid status"}, status=400)

        
        old_status = application.status
        application.status = new_status
        application.save()
        
        if new_status != old_status:
            send_status_notification.delay(
                application.job_seeker.email,       # ايميل الشخص المتقدم
                application.job.title,              # اسم الوظيفة
                new_status                          # الحالة الجديدة
            )
        return Response({"message": f"Status updated to {new_status}"})
    


class RecruiterJobApplicationsCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,pk):
        user = request.user
        if request.user.user_type != "recruiter":
            return Response({"error":"Only recriter can view this"},status=status.HTTP_403_FORBIDDEN) 
        
        try:
            job = Job.objects.get(pk=pk ,recruiter=user)
        except Job.DoesNotExist:
            return Response({"error": "Job not found or you don't have permission to view it."},status= status.HTTP_404_NOT_FOUND) 
        
        count = job.applications.count()
        return Response({
            "job_id": job.id,
            "job_title": job.title,
            "applications_count": count
         })   

class RecruiterAllJobsApplicationsCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]   
    def get(self,request):
        user = request.user
        if request.user.user_type != "recruiter":
            return Response({"error":"Only recruiter can view this"},status=status.HTTP_403_FORBIDDEN) 
        jobs = Job.objects.filter(recruiter=user)

        if not jobs.exists():
            return Response(
                {"message": "You have not posted any jobs yet."},
                status=status.HTTP_200_OK
            )
        data = []
        for job in jobs:
            data.append({
                "job_id": job.id,
                "job_title": job.title,
                "applications_count": job.applications.count()
            })
        total_applications = sum(job.applications.count() for job in jobs)

        return Response({
            "recruiter": user.username,
            "total_jobs": jobs.count(),
            "total_applications": total_applications,
            "jobs": data
        })

            
               