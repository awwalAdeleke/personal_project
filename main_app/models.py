from datetime import datetime, time, date, timedelta

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse, reverse_lazy


# Create your models here.
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(expiry_date__gt=date.today())


class ExpiredManager(models.Manager):
    def get_queryset(self):
        return super(ExpiredManager, self).get_queryset().filter(expiry_date__lt=date.today())


class VisibleManager(models.Manager):
    def get_queryset(self):
        return super(VisibleManager, self).get_queryset().filter(is_hidden=False)


class HiddenManager(models.Manager):
    def get_queryset(self):
        queryset = super(HiddenManager, self).get_queryset()
        return queryset.filter(is_hidden=True)


class EmployeeType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ExperienceLevel(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class JobVacancy(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    company_logo = models.ImageField(max_length=255, upload_to="media/", blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    employee_type = models.ForeignKey(EmployeeType, on_delete=models.SET_NULL, null=True, blank=True)
    experience_level = models.ForeignKey(ExperienceLevel, on_delete=models.SET_NULL, null=True, blank=True)
    description = RichTextUploadingField()
    apply_url = models.URLField(blank=True, null=True)
    expiry_date = models.DateField()
    likes = models.ManyToManyField(User, related_name="job", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active_jobs = ActiveManager()
    expired_jobs = ExpiredManager()

    class Meta:
        ordering = ['created', 'updated']
        verbose_name = 'Job Vacancy'
        verbose_name_plural = 'Job Vacancies'

    def __str__(self):
        return self.position

    def total_likes(self):
        return self.likes.count()

    # @property
    # def is_expired(self):
    #     return bool(self.expiry_date and date.today() > self.expiry_date)

    def get_absolute_url(self):
        return reverse_lazy('job_detail', args=[str(self.pk)])


class Comment(models.Model):
    job_vacancy = models.ForeignKey(JobVacancy, on_delete=models.CASCADE, null=True)
    comment_author = models.CharField(max_length=255)
    comment_message = models.TextField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(default=False)

    objects = models.Manager()
    visible_comments = VisibleManager()
    hidden_comments = HiddenManager()

    def __str__(self):
        return self.comment_message


class Employer(User):
    job_position = models.CharField(max_length=255)
    company = models.CharField(max_length=255)

    class Meta:
        permissions = (('can_create_job', "Can Create Job"),)

