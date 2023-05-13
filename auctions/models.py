from django.contrib.auth.models import AbstractUser
from django.db import models  


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.name}'

# Table containing all the listings
class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=800)
    image_url = models.URLField(blank=True)
    category_id = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    watch_list = models.ManyToManyField(User, blank=True, related_name='watch_list')
    
    def __str__(self):
        return self.title
    
# Table containing bids
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.PositiveIntegerField()

    def __str__(self):
        return f'${self.bid} on {self.listing} by  {self.user}'

# Table containing comments
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)