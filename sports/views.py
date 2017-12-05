# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Create your views here.
import json

from rest_framework import status
from rest_framework.views import APIView
from .serializers import OtpSerializer,UserSerializer,OpportunitySerializer
from .models import Otp,User,UserAuth,Opportunity,Venue
from rest_framework.response import Response
from random import randint
import threading
import urllib2
from django.db import transaction
from .authentication import SimpleMiddleware
from django.utils.decorators import decorator_from_middleware
from django.core.exceptions import ObjectDoesNotExist
import datetime


def sendSMS(formMobile,otp):
    url = "http://control.msg91.com/api/sendhttp.php?"
    url = url + "authkey=112957AN4b64f0a9k57358ac8"
    url = url + "&mobiles="+formMobile
    url = url + "&message=Thanks for registering. Your otp is " + str(otp)
    url = url + "&route=4"
    url = url + "&sender=htiger"
    url = url + "&country=India"
    try:
        response = urllib2.urlopen(url)
        print response.read()
    except Exception as e:
        return  None, e

class GenerateOtp(APIView):
    def post(self, request, format=None):
        newOtp = randint(1000, 9999)
        formMobile = request.data.get('mobile')
        (obj, created) = Otp.objects.update_or_create(
            mobile=formMobile,
            defaults={
                'otp': newOtp
            },
        )
        if not created:
            obj.otp = newOtp
            obj.save(
                update_fields=[
                    'otp',
                ],
            )
        t = threading.Thread(target=sendSMS, args=(formMobile,newOtp), kwargs={}).start()
        return Response(OtpSerializer(obj).data)

class VerifyOtp(APIView):
    def post(self, request, format=None):
        formMobile = request.data.get('mobile')
        formOtp = request.data.get('otp')
        otpRow = Otp.objects.get(mobile=formMobile)
        if otpRow.otp != formOtp:
            return Response("bad otp",status.HTTP_400_BAD_REQUEST,content_type="application/json")
        return Response("otp verified",status.HTTP_200_OK,content_type="application/json")


def getAddress(lat,long):
    base = "http://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={lat},{lon}&sensor={sen}".format(
        lat=lat,
        lon=long,
        sen='false'
    )
    url = "{base}{params}".format(base=base, params=params)
    response = urllib2.urlopen(url)
    tmp = json.loads(response.read())
    if (tmp['status'] != 'OK'):
        return ''
    return  tmp['results'][0]['formatted_address']

class CreateUser(APIView):
    @transaction.atomic
    def post(self, request, format=None):
        try:
            with transaction.atomic():
                user = User()
                user.from_dict(request.data.get('user'))
                try:
                    User.objects.get(email=user.email)
                except ObjectDoesNotExist:
                    if user.address == "":
                        user.address = getAddress(user.lat, user.lng)
                    user.save()
                userFromDB = User.objects.get(email=user.email)
                userAuth = UserAuth()
                userAuth.from_dict(request.data.get('userAuth'))
                userAuth.userID = userFromDB.id
                try:
                    userAuthFromDB = UserAuth.objects.get(userID=userFromDB.id,type=userAuth.type)
                    userAuthFromDB.uniqueId = userAuth.uniqueId
                    userAuthFromDB.save()
                except ObjectDoesNotExist:
                    userAuth.save()
                return Response(UserSerializer(userFromDB).data)
        except Exception as e:
            return Response({"message": "invalid post request to create user."}, status.HTTP_400_BAD_REQUEST, content_type="application/json")

class LoginUser(APIView):
    @transaction.atomic
    def post(self,request,format=None):
        try:
            with transaction.atomic():
                formEmail = request.data.get('email')
                userFromDB = User.objects.get(email=formEmail)
                userAuth = UserAuth()
                userAuth.from_dict(request.data.get('userAuth'))
                UserAuth.objects.get(userID=userFromDB.id,
                                                      type=userAuth.type,
                                                      uniqueId=userAuth.uniqueId)
                return Response(UserSerializer(userFromDB).data)
        except Exception:
            return Response({"message": "invalid login details."}, status.HTTP_401_UNAUTHORIZED, content_type="application/json")

class CreateOpportunity(APIView):
    @decorator_from_middleware(SimpleMiddleware)
    @transaction.atomic
    def post(self,request,format=None):
        try:
            with transaction.atomic():
                currentUser = User.objects.get(id=request.data.get('userId'))
                opportunity = Opportunity()
                opportunity.from_dict(request.data)
                venue = Venue.objects.get_or_create(id=1,
                                                    defaults={
                                                        'deleted': False,
                                                        'lat': currentUser.lat,
                                                        'lng': currentUser.lng,
                                                        'address': currentUser.address
                                                    })
                opportunity.venue = venue[0]
                opportunity.creator = currentUser
                opportunity.save()
                return Response(OpportunitySerializer(opportunity).data)
        except Exception as e:
            return Response({"message": e}, status.HTTP_400_BAD_REQUEST, content_type="application/json")

class Follow(APIView):
    @decorator_from_middleware(SimpleMiddleware)
    @transaction.atomic
    def post(self, request, format=None):
        try:
            with transaction.atomic():
                currentUser = User.objects.get(id=request.data.get('userId'))
                currentUser.follows.add(request.data.get('userToFollowId'))
                currentUser.save()
                return Response({"message": "successfull"}, status.HTTP_200_OK, content_type="application/json")
        except Exception as e:
            return Response({"message": "invalid follow request"}, status.HTTP_400_BAD_REQUEST, content_type="application/json")

class GetFollowers(APIView):
    def post(self, request, format=None):
        try:
            currentUser = User.objects.get(id=request.data.get('userId'))
            return Response(UserSerializer(currentUser.follows.all(),many=True).data)
        except Exception as e:
            return Response({"message": e}, status.HTTP_400_BAD_REQUEST,
                        content_type="application/json")





