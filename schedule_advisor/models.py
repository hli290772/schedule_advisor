from django.db import models
from django.contrib.auth.models import User
import datetime
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import admin
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Subject(models.Model):
   abbreviation = models.CharField(max_length=100) # CS
   description = models.CharField(max_length=100) # Computer Science
   def __str__(self):
      return self.abbreviation

class Course(models.Model):
   class_section = models.CharField(max_length=100, default="0")
   class_nbr = models.CharField(max_length=100, default="0")
   subject = models.CharField(max_length=100, default="0")
   catalog_nbr = models.CharField(max_length=100, default="0")
   wait_tot = models.CharField(max_length=100, default="0")
   wait_cap = models.CharField(max_length=100, default="0")
   class_capacity = models.CharField(max_length=100, default="0")
   enrollment_total = models.CharField(max_length=100, default="0")
   enrollment_available = models.CharField(max_length=100, default="0")  
   descr = models.CharField(max_length=100, default="0")  
   units = models.CharField(max_length=100, default="0") 
   instructor_name = models.CharField(max_length=100, default="0") 
   meetings_days = models.CharField(max_length=100, default="0") 
   meetings_start_time = models.CharField(max_length=100, default="0") 
   meetings_end_time = models.CharField(max_length=100, default="0") 
   meetings_facility_descr = models.CharField(max_length=100, default="0") 
    
   def __str__(self):
      return self.subject + self.catalog_nbr + " " + self.class_section

class Profile(models.Model):    
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   courses = models.ManyToManyField(Course)

   is_advisor = models.BooleanField(default=False)
   advisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="advisee",null=True)
   approved = models.BooleanField(default=False)

   @receiver(post_save, sender=User)
   def create_user_profile(sender, instance, created, **kwargs):
      if created:
         Profile.objects.create(user=instance)

   @receiver(post_save, sender=User)
   def save_user_profile(sender, instance, **kwargs):
      instance.profile.save()
   
   def __str__(self):
      return self.user.username
