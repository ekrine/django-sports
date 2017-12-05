from rest_framework import serializers
from .models import Otp, User, Opportunity

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','name','date_created','date_modified',
                 'status','role','email','mobile','imageUrl',
                 'oneLiner','address','lat','lng')
        read_only_fields = ('id','date_created', 'date_modified','email')


class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = '__all__'
        read_only_field = ('id')

class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ('mobile','otp')
        read_only_field = ('mobile')
