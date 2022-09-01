from django.contrib import admin

from .models import Comment, EmployeeType, ExperienceLevel, Location, JobVacancy
# Register your models here.


admin.site.register(Comment)
admin.site.register(EmployeeType)
admin.site.register(ExperienceLevel)
admin.site.register(Location)
admin.site.register(JobVacancy)
