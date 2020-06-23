from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from collegeapp import models

# Register your models here.
admin.site.register(models.College)
admin.site.register(models.Course)
admin.site.register(models.Comment)
admin.site.register(models.Location)