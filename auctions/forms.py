from django import forms
from .models import *

# Project ModelForms
#-------------------

# Note that the user_id is not added to the forms so that the information in the User model is not sent to any user creating a listing

# Model form for user to enter the listings
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'image_url']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "Title (required)"}),
            'description': forms.Textarea(attrs={'placeholder': "Description (required)"}),
            'image_url': forms.TextInput(attrs={'placeholder': "Image URL"})
            }

# Model form for user to create a bid
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']
        widgets = {
            'bid': forms.NumberInput(attrs={'placeholder': 'Initial bid', 'size': '8'})
        }
# Model form for user to create a Category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Category'}),
        }

# Model form for user to create a Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Add comment'}),
        }