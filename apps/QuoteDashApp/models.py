from __future__ import unicode_literals
from django.db import models

import bcrypt
import re 

EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX=re.compile(r'^[a-zA-Z\s]$')

class ValidationManager(models.Manager):
    def registration_validator(self,postData):
        errors={}
        if len(postData['txtFirst'])<1 or NAME_REGEX.match(postData['txtFirst']):
            errors['fName']="First name should be letters only."
        if len(postData['txtLast'])<1 or NAME_REGEX.match(postData['txtLast']):
            errors['lName']="Last name should be letters only."
        if not EMAIL_REGEX.match(postData['txtEmail']):
            errors['eMail']="Invalid eMail address."
        if len(Users.objects.filter(email_address=postData['txtEmail']))>0:
            errors['dupEmail']="duplicate email detected."
        if len(postData['txtPWord'])<8 and len(postData['txtPWord'])>25:
            errors['pwLen']="Password should be atleast 8 and not more than 25 characters."
        if postData['txtPWord'] != postData['txtConWord']:
            errors['pwMatch']="Passwords did not match."
        return errors
    
    def login_validator(self,postData):
        validator={}
        users=Users.objects.filter(email_address=postData['txtUMail'])
        match=False
        if len(users)>0:
            for user in users:
                if bcrypt.checkpw(postData['txtUPWord'].encode(),user.password.encode()):
                    match=True
                    validator['match']=match
                    validator['ID']=user.id
            if not match:
                validator['noMatch']="eMail and password did not match."
        else:
            validator['noEmail']="eMail does not exist."
        return validator

    def post_validator(self,postData):
        validator={}
        if len(postData['txtAuthor'])<=3:
            validator['author']="Author must be more than 3 characters"
        if len(postData['txtQuote'])<=3:
            validator['author']="Author must be more than 3 characters"
        return validator

    def edit_user_validator(self,postData):
        errors={}
        if len(postData['txtFirst'])<1 or NAME_REGEX.match(postData['txtFirst']):
            errors['fName']="First name should be letters only."
        if len(postData['txtLast'])<1 or NAME_REGEX.match(postData['txtLast']):
            errors['lName']="Last name should be letters only."
        if not EMAIL_REGEX.match(postData['txtEmail']):
            errors['eMail']="Invalid eMail address."
        if len(Users.objects.filter(email_address=postData['txtEmail']))>0:
            errors['dupEmail']="duplicate email detected."
        
        return errors

class Users(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email_address=models.CharField(max_length=255)
    password=models.CharField(max_length=25)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects=ValidationManager()

class Quotes(models.Model):
    message=models.TextField()
    author=models.CharField(max_length=255)
    posted_by=models.ForeignKey(Users,related_name="quote")
    liked_by=models.ManyToManyField(Users,related_name="liked")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects=ValidationManager()