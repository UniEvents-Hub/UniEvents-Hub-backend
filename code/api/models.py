from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields
    interests = models.CharField(max_length=255, blank=True, null=True)  # You can consider using ArrayField for PostgreSQL
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255,blank=True, null=True)
    city = models.CharField(max_length=100,blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    
    # Billing address fields
    billing_address1 = models.CharField(max_length=255, blank=True, null=True)
    billing_address2 = models.CharField(max_length=255, blank=True)
    billing_city = models.CharField(max_length=100, blank=True, null=True)
    billing_zipcode = models.CharField(max_length=10, blank=True, null=True)
    billing_province = models.CharField(max_length=100, blank=True, null=True)
    
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)


    def __str__(self):
        return self.user.username
