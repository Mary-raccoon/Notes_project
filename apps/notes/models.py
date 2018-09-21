from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name'])< 3:
            errors['name'] = "Name should be at least 2 characters"
        elif not 'name' in errors and not re.match(NAME_REGEX, postData['name']):
            errors['name'] = "Name must only contain letters"
        if not 'email' in errors and not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "Email is invalid"
        if len(postData['password'])< 8:
            if len(postData['password'])< 1:
                errors['password'] = "Password can't be blank"
            errors['password'] = "Password should be no fewer than 8 characters in length"
        if postData['conf_password'] != postData['password']:
            errors['conf_password'] = "Passwords do not match"
        return errors
        
    def login_validator(self, postData):
        errors = {}
        if len(postData['email1']) < 1:
            errors['email1'] = "Not a valid email"
        if len(User.objects.filter(email=postData['email1'])) == 0:
            errors['email1'] = "Email does not exist. Register first!"
        if len(User.objects.filter(email=postData['email1'])) == 1:
            password_hash = User.objects.get(email=postData['email1']).password
            if bcrypt.checkpw(postData['password1'].encode(), password_hash.encode()) == False:  
                errors['password1'] = "Incorrect password. Try again!"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255, blank=False)
    email = models.CharField(max_length=255, unique=True )
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return "<User_object: {} {}>".format(self.name, self.email)

class NoteManager(models.Manager):
    def note_validator(self, postData):
        errors = {}
        if len(postData['label']) < 3:
            errors['label'] = "Label should be more then 3 characters"
        if len(postData['desc']) < 11:
            errors['desc'] = "Description should be more then 10 characters"
        return errors
        
class Note(models.Model):
    label = models.CharField(max_length=255, blank=False)
    desc = models.TextField(blank=False)
    author = models.ForeignKey(User, related_name="notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = NoteManager()

    def __repr__(self):
        return "<Job_object: {} {} {} {} {}>".format(self.label, self.desc, self.author)
