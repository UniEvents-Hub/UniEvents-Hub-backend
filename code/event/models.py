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
    event_type = models.CharField(max_length=100, default='music', blank=True, null=True)
    banner = models.ImageField(upload_to=upload_to, blank=True, null=True)  
    title = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True) 
    end_time = models.TimeField( blank=True, null=True)   
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ticket_type = models.CharField(max_length=50, blank=True, null=True)
    sharable_link = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True) 
    total_tickets = models.IntegerField(blank=True, null=True)  
    event_status = models.CharField(max_length=50, blank=True, null=True)     
    
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
    

class Saved(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Saved for {self.event.title} owned by {self.user.username}"