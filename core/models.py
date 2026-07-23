from django.db import models
from django.contrib.auth.models import User

class BandProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    
    genres = models.CharField(max_length=255, blank=True, help_text="Odvojite žanrove zarezom.")
    influences = models.TextField(blank=True)
    
    looking_for_members = models.BooleanField(default=False)
    needed_members_description = models.TextField(blank=True, help_text="Opišite koga tražite...")
    
    available_for_gigs = models.BooleanField(default=True)
    
    song1 = models.FileField(upload_to='bend_songs/', null=True, blank=True)
    song2 = models.FileField(upload_to='bend_songs/', null=True, blank=True)
    
    contact_email = models.EmailField(blank=True)
    spotify_link = models.URLField(blank=True)
    youtube_link = models.URLField(blank=True)
    facebook_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} Profile'
    
    
class AddGigDate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    local_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    date = models.DateField()   
    time = models.TimeField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'${self.user}'
    
    
class SendMessageToBand(models.Model):
    band_profile = models.ForeignKey(BandProfile, on_delete=models.CASCADE)
    sender_name = models.CharField(max_length=100, blank=True, null=True)
    sender_email = models.EmailField( blank=True, null=True) 
    phone_contact = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Message to {self.band_profile} from {self.sender_name}'