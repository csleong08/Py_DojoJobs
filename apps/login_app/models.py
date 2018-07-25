from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email
from datetime import date
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 3 or any(i.isdigit() for i in postData['first_name']):
            errors['first_name'] = "First name should be at least 2 characters with no numbers"
        if len(postData['last_name']) < 2 or any(i.isdigit() for i in postData['first_name']):
            errors['last_name'] = "Last name should be at least 2 characters with no numbers"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm_pw'] :
            errors['password'] = "Passwords do not match"
        if len(postData['email']) < 1:
            errors['email'] = "Email field is empty"
        elif not EMAIL_REGEX.match(postData['email']): 
            errors['email'] = "Invalid email address"
        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        # print(user)
        if len(postData['email']) < 1:
            errors['email'] = "Login email field is empty"
        elif not EMAIL_REGEX.match(postData['email']): 
            errors['email'] = "Invalid email address format"
        elif len(user) < 1:
            errors['email'] = "Email address is not registered"
        if len(postData['password']) < 8:
            errors['password'] = "Login password should be at least 8 characters"
        return errors

class JobManager(models.Manager):
    def job_validator(self, postData):
        errors = {}
        if len(postData['job_name']) < 3:
            errors['job_name'] = "Job Title field should be at least 3 characters"
        if len(postData['location']) < 1:
            errors['location'] = "Location field is empty"
        if len(postData['desc']) < 10:
            errors['desc'] = "Description field should be at least 10 characters"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Job(models.Model):
    job_name = models.CharField(max_length=255)
    desc = models.TextField(max_length=1000)
    location = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="created_jobs")
    liked_users = models.ManyToManyField(User, related_name="liked_jobs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()