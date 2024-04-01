from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated  # Import AllowAny permission
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from .models import Event, Ticket
from .serializers import EventSerializer, TicketSerializer
from rest_framework.response import Response
import json
from rest_framework.generics import UpdateAPIView
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework import permissions
import base64
from django.core.files.base import ContentFile

class IsEventCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user making the request is the creator of the event
        return obj.user.id == request.user.id

class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for creating events
    #authentication_classes = [SessionAuthentication]  # Use session authentication

    def perform_create(self, serializer):
        # Automatically set the user to the currently authenticated user
        serializer.save(user=self.request.user)

class EventRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]  # Allow access to any user

    def get(self, request):
        try:
            filter_column_value = request.query_params.get('event_id')
        except ValueError:
            return Response({'error': 'Invalid filter_column_value'}, status=400)
        
        if filter_column_value:
            queryset = Event.objects.filter(id=filter_column_value)
            serializer = EventSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'No filter_column_value provided'}, status=400)

class UserEventRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsEventCreator]  # Require authentication and check if the user is the event creator

    def get(self, request):
        try:
            filter_column_value = request.query_params.get('user_id')
        except ValueError:
            return Response({'error': 'Invalid filter_column_value'}, status=400)
        
        if filter_column_value:
            queryset = Event.objects.filter(user=filter_column_value)
            serializer = EventSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'No filter_column_value provided'}, status=400)


class EventUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsEventCreator]  # Require authentication and check if the user is the event creator
    serializer_class = EventSerializer

    def get_object(self):
        event_id = self.kwargs.get('pk')  # Get event ID from URL argument
        if event_id is None:
            raise NotFound('Event ID is required.')
        try:
            return Event.objects.get(pk=event_id)  # Get event object by ID
        except Event.DoesNotExist:
            raise NotFound('Event with this ID does not exist.')

    def partial_update(self, request, *args, **kwargs):
        # No changes required here, logic remains the same for patching the retrieved object
        instance = self.get_object()
        base64_image = request.data.get('banner', None)
        if base64_image:
            # Decode the base64 image data
            image_data = base64.b64decode(base64_image)

            # Create a ContentFile instance with the image data
            file_name = f"{instance.id}_event_banner.png"
            content_file = ContentFile(image_data, name=file_name)

            # Update the request data with the ContentFile instance
            request.data['banner'] = content_file
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            filter_column_value = request.query_params.get('event_type')
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON data'}, status=400)
        
        # Fetch all rows of the desired table
        if filter_column_value:
            # Filter the queryset based on the filter column value
            queryset = Event.objects.filter(event_type=filter_column_value)
        else:
            # No filter parameter provided, return all rows
            queryset = Event.objects.all()
        
        # Serialize the queryset
        serializer = EventSerializer(queryset, many=True)
        
        # Return the serialized data as JSON
        return Response(serializer.data)
    
    
class TicketCreateAPIView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]  # Adjust permissions as needed
    
    
class UserTicketAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        try:
            filter_column_value = request.query_params.get('user_id')
        except ValueError:
            return Response({'error': 'Invalid user id'}, status=400)
        
        if filter_column_value:
            queryset = Ticket.objects.filter(user=filter_column_value)
            serializer = TicketSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'No user id provided'}, status=400)