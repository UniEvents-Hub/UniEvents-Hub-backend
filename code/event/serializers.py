from rest_framework import serializers
from .models import Event, Ticket, Saved

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        
        
class SavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saved
        fields = '__all__'