# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
        
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

    def test_api_can_create_a_user(self):
        """Test the api has user creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        
    def test_api_can_get_a_user(self):
        """Test the api can get a user."""
        user = User.objects.get()
        response = self.client.get(
            reverse('details',
            kwargs={'pk': user.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, user)

    def test_api_can_update_bucketlist(self):
        """Test the api can update a user."""
        user = User.objects.get()
        change_user = {'name': 'Something new'}
        res = self.client.put(
            reverse('details', kwargs={'pk': user.id}),
            change_user, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_bucketlist(self):
        """Test the api can delete a user."""
        user = User.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': user.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)