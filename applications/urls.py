from django.urls import path
from .views import ApplicationView , ApplicationsForRecruiterView , RecruiterJobApplicationsCountView , RecruiterAllJobsApplicationsCountView

urlpatterns = [
    path('', ApplicationView.as_view(), name='applications'),
    path('job/', ApplicationsForRecruiterView.as_view(), name='recruiter_applications'),
    path('<int:pk>/update-status/', ApplicationsForRecruiterView.as_view(), name='update_application_status'),
    path('jobs/<int:pk>/applications/count/', RecruiterJobApplicationsCountView.as_view(), name='recruiter-job-applications-count'),
    path('jobs/company/all-applications-count/', RecruiterAllJobsApplicationsCountView.as_view(), name='recruiter-all-jobs-applications-count'),

]
