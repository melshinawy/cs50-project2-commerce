from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'seller', 'category')

class BidAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'bid')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'comment')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)