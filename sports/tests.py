# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse

# Create your tests here.
class ModelTestCase(TestCase):
    def setup(self):
        self.user_name = "test user"
        self.User = User(name=self.user_name)
    
    def test_model_can_create_a_user(self):
        old_count = User.objects.count()
        self.User.save()
        new_count = User.objects.count()
        self.assertNotEqual(old_count,new_count)
        
class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.user_data = {'name': 'Rahul Yadav'}
        self.response = self.client.post(
            reverse('create'),
            self.user_data,
            format="json")

    def test_api_can_create_a_bucketlist(self):
        """Test the api has bucket creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)