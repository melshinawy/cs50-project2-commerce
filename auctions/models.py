from django.contrib.auth.models import AbstractUser
from django.db import models  


class User(AbstractUser):
    pass

# Table containing all the listings
class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=800)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=32, blank=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
# Table containing bids
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.PositiveIntegerField()

# Table containing comments
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)