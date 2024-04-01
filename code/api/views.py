from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics 
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UserProfile
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from six import text_type
from rest_framework.generics import UpdateAPIView,RetrieveUpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound
import json
import base64
from django.core.files.base import ContentFile

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            user = serializer.instance
            UserProfile.objects.create(user=user)
            tokens = RefreshToken.for_user(user)
            data = {
                "refresh": str(tokens),
                "access": str(tokens.access_token)
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserProfileAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]  # Require authentication for listing and creating user profiles
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        user_id = self.kwargs.get('pk')  # Get event ID from URL argument
        if user_id is None:
            raise NotFound('User ID is required.')
        try:
            return UserProfile.objects.get(user=user_id)  # Get event object by ID
        except UserProfile.DoesNotExist:
            raise NotFound('User with this ID does not exist.')
    
    def custom_get_object(self):
        user_id = self.kwargs.get('pk')  # Get event ID from URL argument
        if user_id is None:
            raise NotFound('User ID is required.')
        try:
            return User.objects.get(pk=user_id)  # Get event object by ID
        except UserProfile.DoesNotExist:
            raise NotFound('User with this ID does not exist.')
    
    def partial_update(self, request, *args, **kwargs):
        # No changes required here, logic remains the same for patching the retrieved object
        instance = self.get_object()
        base64_image = request.data.get('profile_photo', None)
        if base64_image:
            # Decode the base64 image data
            image_data = base64.b64decode(base64_image)

            # Create a ContentFile instance with the image data
            file_name = f"{instance.user.username}_profile_photo.png"
            content_file = ContentFile(image_data, name=file_name)

            # Update the request data with the ContentFile instance
            request.data['profile_photo'] = content_file
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        temp1 = {"profile":serializer.data}
        instance = self.custom_get_object()
        serializer = UserSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        temp2 = {"user":serializer.data}
        response_data = {**temp1, **temp2}
        return Response(response_data, status=status.HTTP_200_OK)
    
class UserProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # Retrieve the UserProfile instance
        # Retrieve the related User instance
        user_serializer = UserSerializer(instance)  
        

        # Serialize UserProfile instance
        profile_serializer = UserProfileSerializer(instance.userprofile)  

        # Combine data from both serializers
        data = {
            'user': user_serializer.data,
            'profile': profile_serializer.data
        }

        return Response(data)
