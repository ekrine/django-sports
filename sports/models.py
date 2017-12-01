# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
    name = models.CharField(max_length=255, blank=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    role = models.IntegerField(choices=ROLE_CHOICES, default=2)
    
    
    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)