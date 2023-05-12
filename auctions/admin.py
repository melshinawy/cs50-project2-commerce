from django.contrib import admin
from .models import *

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category')

class BidAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'bid')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'comment')

# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)