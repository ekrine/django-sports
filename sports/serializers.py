from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','name','date_created','date_modified',
                 'status','role')
        read_only_fields = ('id','date_created', 'date_modified')
