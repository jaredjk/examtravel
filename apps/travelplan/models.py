from __future__ import unicode_literals
import re, bcrypt, datetime
from django.db import models


NAME_REGEX = re.compile(r'^[a-zA-Z]\w+$')

class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors["name"] = "Name fewer than 3 characters"
        if len(postData['username']) < 3:
            errors["username"] = "Username cannot be fewer than 3 characters"
        if not re.match(NAME_REGEX, postData['name']):
            errors["name"] = "Name can have only letters"
        if not re.match(NAME_REGEX, postData['username']):
            errors["username"] = "Username can have only letters"
        if len(postData['password']) < 8:
            errors["password_length"] = "Password must be at least 8 characters long"
        if postData['password'] != postData['confirm_password']:
            errors["password"] = "Password must match"
        return errors
    
    def validate_login(self, postData):
        errors=[]
        if len(self.filter(username=postData['username'])) > 0:
            user = self.filter(username=postData['username'])[0]
            if not (bcrypt.hashpw(postData['password'].encode(), user.password.encode())):
                errors.append('Email and password does not match')
        else:
            errors.append('Email and password does not match')
        if errors:
            return errors
        return user 

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class TripManage(models.Manager):
    def validate_trip(self, postData):
        errors={}
        if len(postData['destination']) < 1:
            errors["destination"] = "Please enter Destination of the trip"
        if len(postData['description']) < 1:
            errors["description"] = "Please enter Description of the trip"
        if (postData['traveldatefrom'] < str(datetime.date.today())):
            errors["traveldatefrom"] = "Travel dates should be future-dated"
        if (postData['traveldateto'] < postData['traveldatefrom']):
            errors["traveldateto"] = "Travel Date To should not be before the Travel Date From"
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    traveldatefrom = models.DateField(auto_now=False, auto_now_add=False)
    traveldateto = models.DateField(auto_now=False, auto_now_add=False)
    tripcreater = models.ForeignKey(User, related_name='tripcreated')
    tripjoiners = models.ManyToManyField(User, related_name='tripsgoingto')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManage()