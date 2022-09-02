from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import home, create_job, JobListView, job_detail,\
    hide_comment, login_page, logout_page, register_user, like_view, EmployerJobListView

urlpatterns = [
    path('home/', home, name='home'),
    path('add_job/', create_job, name='add_job'),
    path('my_jobs/', EmployerJobListView.as_view(), name='employer_job_list'),
    path('jobs/', JobListView.as_view(), name='job_list'),
    path('jobs/job-<int:pk>/', job_detail, name='job_detail'),
    # path('jobs/job-<int:pk>/add_comment', add_comment, name='add_comment'),
    path('jobs/job-<int:pk>/hide_comment/', hide_comment, name='hide_comment'),
    path('jobs/job-<int:pk>/like_job', like_view, name='like_job'),

    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('employer/register', register_user, name='employer_register'),
    path('applicant/register', register_user, name='applicant_register'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
