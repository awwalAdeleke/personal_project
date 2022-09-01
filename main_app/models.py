from datetime import datetime, time, date, timedelta

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(is_expired=False)


class ExpiredManager(models.Manager):
    def get_queryset(self):
        return super(ExpiredManager, self).get_queryset().filter(is_expired=True)


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
    description = RichTextField()
    expiry_date = models.DateField()
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

    @property
    def is_expired(self):
        return bool(self.expiry_date and date.today() > self.expiry_date)

    def get_absolute_url(self):
        return reverse('job_detail')


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

