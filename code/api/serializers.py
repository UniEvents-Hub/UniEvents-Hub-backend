from django.contrib.auth.models import User 
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken



from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password","email", "first_name", "last_name"]
        extra_kwargs = {"password":{"write_only":True}, "email":{"required":True}, "first_name":{"required":True}, "last_name":{"required":True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    
    


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'