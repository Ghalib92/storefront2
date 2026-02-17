from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import User    

class UserCreateSerializer(BaseUserCreateSerializer):
     


    class Meta(BaseUserCreateSerializer.Meta):
        
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password' )