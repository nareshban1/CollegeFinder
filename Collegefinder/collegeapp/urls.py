from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('colleges/', views.colleges, name='colleges'),
    path('details/(<id>)/', views.details, name='details'),
    path('colleges/(<id>)/', views.course_college, name='course_college'),
    path('location/(<id>)/', views.location, name='location'),
    path('results/', views.search, name='search'),
    path('(<id>)/favourite/', views.favourite, name='favourite'),
    path('favourites/', views.favourite_list, name='favourites'),
    path('contact/', views.contact, name='contact'),

]