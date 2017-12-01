# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#efrom django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializers import UserSerializer
from .models import User

class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = User.objects.all()
    serializer_class = UserSerializer