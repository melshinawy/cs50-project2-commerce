from django.contrib.auth.models import AbstractUser
from django.db import models  


class User(AbstractUser):
    pass

# Model containing the categories
class Category(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

# Model containing all the listings
class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=800)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name='watchlist')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='winner')
    
    def __str__(self):
        return self.title
    
# Model containing bids
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.FloatField()

    def __str__(self):
        return f'${self.bid} on {self.listing} by  {self.user}'

# Model containing comments
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)