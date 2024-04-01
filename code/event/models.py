from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from django.db import models
from django.contrib.auth.models import User

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    event_type = models.CharField(max_length=100, default='music')
    banner = models.ImageField(upload_to=upload_to, blank=True, null=True)  
    title = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True) 
    end_time = models.TimeField(null=True, blank=True)   
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    ticket_type = models.CharField(max_length=50)
    sharable_link = models.URLField()
    address = models.CharField(max_length=255) 
    total_tickets = models.IntegerField()       
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Get the current user from the session
        user = self._get_user_from_session()

        # Assign the current user to the 'user' field
        if user and isinstance(user, get_user_model()):
            self.user = user

        # Call the original save method
        super().save(*args, **kwargs)

    def _get_user_from_session(self):
        # Implement your logic to retrieve the current user from the session
        # This might involve accessing the request object in the view
        # Here, we assume you have access to the request object
        if hasattr(self, '_request'):
            return self._request.user
        else:
            return AnonymousUser()  # Return AnonymousUser if request object is not available

class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_number = models.IntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Ticket for {self.event.title} owned by {self.user.username}"