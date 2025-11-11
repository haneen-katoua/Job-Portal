from django.urls import path
from .views import JobView , SavedJobView , NotificationView

urlpatterns = [
    path('create/', JobView.as_view(),name='create job'),          # GET all, POST create
    path('update/<int:pk>/', JobView.as_view() , name='update job'),# GET one, PUT update, DELETE 
    path('all-jobs/',JobView.as_view(),name = 'get all jobs'),
    path('retrieve/<int:pk>/',JobView.as_view(),name='retreive job'),
    path('delete/<int:pk>/',JobView.as_view(),name='delete job'),
    path('<int:job_id>/save/', SavedJobView.as_view(), name='save-job'),
    path('saved-jobs/', SavedJobView.as_view(), name='saved-jobs'),
    path('saved-jobs/<int:pk>/delete/', SavedJobView.as_view(), name='remove-saved-job'),
    path('notifications/',NotificationView.as_view(),name='notifications'),
    path('notifications/<int:pk>/read/',NotificationView.as_view(),name='is_read'),

]
