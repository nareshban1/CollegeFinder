from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models import options

class Course(models.Model):
    coursename = models.CharField('Course Name', max_length=120)
    shortname = models.CharField('Cname', max_length=10)

    def __str__(self):
        return self.shortname

class Location(models.Model):
    locationname = models.CharField('Location Name', max_length=120,default="...")

    def __str__(self):
        return self.locationname

class College(models.Model):
    collegename = models.CharField('College Name', max_length=120)
    description = models.TextField()
    image = models.ImageField(upload_to='college_images')
    courses= models.ManyToManyField(Course, related_name='courses')
    address= models.CharField(max_length=120, default="...")
    location = models.ForeignKey(Location, default=4, on_delete=models.SET_DEFAULT, related_name='location')
    contact_no = models.CharField(max_length=120, default="Not available")
    Email = models.CharField(max_length=120, default="...")
    Website = models.CharField(max_length=120, default="...")
    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)
    affiliation = models.CharField(max_length=120, default="...")

    def __str__(self):
        return self.collegename



class Comment(models.Model):
    college= models.ForeignKey(College, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=160)
    rating = models.IntegerField(blank=True, null=True, validators=[ MaxValueValidator(5), MinValueValidator(1)])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return '{}-{}-{}'.format(self.college.collegename, str(self.user.username), self.timestamp)


