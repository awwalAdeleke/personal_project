from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import home, create_job, JobListView, job_detail, hide_comment, login_page, logout_page, register_user

urlpatterns = [
    path('home/', home, name='home'),
    path('add_job/', create_job, name='add_job'),
    path('jobs/', JobListView.as_view(), name='job_list'),
    path('jobs/job-<int:pk>/', job_detail, name='job_detail'),
    path('jobs/job-<int:pk>/hide_comment/', hide_comment, name='hide_comment'),

    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register', register_user, name='register'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
