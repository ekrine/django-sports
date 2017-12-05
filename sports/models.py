# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import models

# Create your models here.
class User(models.Model):
    ACTIVE = 1
    INACTIVE = 2
    REGISTERED = 3
    DEACTIVATED = 4
    WAITING_FOR_APPROVAL = 5

    STATUS_CHOICES = (
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE'),
        (REGISTERED, 'REGISTERED'),
        (DEACTIVATED,'DEACTIVATED'),
        (WAITING_FOR_APPROVAL,'WAITING_FOR_APPROVAL')
    )

    ROLE_CHOICES = (
        (1, 'SELLER'),
        (2, 'ACCOUNT'),
        (3, 'ADMIN')
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    role = models.IntegerField(choices=ROLE_CHOICES, default=2)
    password = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=70, null=False, blank=False, unique=True)
    mobile = models.CharField(max_length=255, blank=False)
    imageUrl = models.CharField(max_length=255, blank=False)
    oneLiner = models.CharField(max_length=255, blank=False)
    address = models.CharField(max_length=255, blank=True)
    lat = models.DecimalField(decimal_places=10, max_digits=20)
    lng = models.DecimalField(decimal_places=10, max_digits=20)
    follows = models.ManyToManyField('self',blank=True,symmetrical=False,related_name='followed_by')

    def __str__(self):
        return "{}".format(self.name)

    def from_dict(self,j):
        self.__dict__.update(j)

class UserAuth(models.Model):
    ACCOUNT_TYPES = (
        (1, 'FACEBOOK'),
        (2, 'GOOGLE'),
        (3, 'MANUAL')
    )
    userID = models.BigIntegerField(null=False)
    uniqueId = models.CharField(max_length=255,null=False,blank=False)
    type = models.IntegerField(choices=ACCOUNT_TYPES,default=3)

    def from_dict(self,j):
        self.__dict__.update(j)
    
class Otp(models.Model):
    mobile = models.CharField(max_length=11,null=False,blank=False,unique=True)
    otp = models.IntegerField(blank=False)

    def __str__(self):
         return "{}".format(self.mobile)


class Venue(models.Model):
    address = models.CharField(max_length=255, blank=True)
    lat = models.DecimalField(decimal_places=10, max_digits=20)
    lng = models.DecimalField(decimal_places=10, max_digits=20)
    creator = models.ForeignKey(User)
    deleted = models.BooleanField(null=False,default=False)

    def from_dict(self,j):
        self.__dict__.update(j)

class Opportunity(models.Model):
    sportId = models.IntegerField(null=False)
    price = models.DecimalField(decimal_places=10, max_digits=20)
    date = models.BigIntegerField(null=False,blank=True)
    startTime = models.BigIntegerField(null=False,blank=True)
    endTime = models.BigIntegerField(null=False,blank=True)
    creator = models.ForeignKey(User,null=False,related_name='creator')
    acceptor = models.ForeignKey(User,null=True,related_name='acceptor')
    requstors = models.ManyToManyField(User,related_name='requestors')
    venue = models.ForeignKey(Venue)
    deleted = models.BooleanField(null=False,default=False)
    instructions = models.TextField()
    sponsor = models.IntegerField(null=True)

    def from_dict(self,j):
        self.__dict__.update(j)
