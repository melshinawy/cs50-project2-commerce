from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Max
from django.urls import reverse
from django.forms import modelform_factory
from .forms import *
from .models import *
from .helper_functions import get_max_bids


def index(request):
    # Create QuerySets for the active listings and maximum bid 
    active_listings = Listing.objects.exclude(active=False).all()

    # Create a dict to map active listings with highest bid
    context = {
        'title': 'Active Listings',
        'listings': get_max_bids(active_listings)
    }

    return multiple_listings(request, context)

def multiple_listings(request, context):
    for listing in context['listings']:
        if not listing.image_url:
            listing.image_url = 'https://st4.depositphotos.com/14953852/24787/v/450/depositphotos_247872612-stock-illustration-no-image-available-icon-vector.jpg'

    return render(request, "auctions/index.html", context)

def categories(request):
    all_categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        'categories': all_categories
    })

def category_name(request, category_id):

    category = Category.objects.get(pk=category_id)
    listings = Listing.objects.filter(category_id=category.id)
    listings = listings.filter(active=True)
    
    context = {
        'title': category.name,
        'listings': get_max_bids(listings)
    }

    return multiple_listings(request, context)

@login_required
def watchlist(request):
    user = User.objects.get(pk=request.user.id)
    watchlist = user.watchlist.all()
    context = {
        'title': 'Watchlist',
        'listings': get_max_bids(watchlist)
    }
    return multiple_listings(request, context)

def listing_page(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user_id = request.user.id
    if request.method == 'GET':

        max_bid = Bid.objects.filter(listing=listing_id).aggregate(Max('bid'))['bid__max']
        context = {
                'listing': Listing.objects.get(pk=listing_id),
                'max_bid': max_bid,
                'user_id': user_id,
                'comments': Comment.objects.filter(listing=listing)
            }

        if user_id:
            user = User.objects.get(pk=request.user.id)

            if listing.seller.id == user.id:
                listing_manipulation = 'Close auction'
            elif listing in user.watchlist.all():
                listing_manipulation = 'Remove from watchlist'
            else:
                listing_manipulation = 'Add to watchlist'
            
            context['listing_manipulation'] = listing_manipulation

            if listing.active:
                context['comment_form'] = CommentForm()
            
            if (listing.seller != user):
                form = modelform_factory(Bid, form=BidForm, widgets={'bid': forms.NumberInput(attrs={'placeholder': 'Bid', 'size': '8', 'min': max_bid + 0.01})})

                context['bid_form'] = form
    
        return render(request, "auctions/listing_page.html", context)

    else:
        bid_f = BidForm(request.POST)
        comment_f = CommentForm(request.POST)

        if 'bid' in request.POST :
            new_bid = bid_f.save(commit=False)
            new_bid.listing = listing
            new_bid.user = User.objects.get(pk=user_id)
            new_bid.save()
        elif 'comment' in request.POST:
            new_comment = comment_f.save(commit=False)
            new_comment.listing = listing
            new_comment.user = User.objects.get(pk=user_id)
            new_comment.save()
        else:
            return render(request, 'auctions/error.html')

        return HttpResponseRedirect(reverse('listing_page', args=(listing_id,)))

@login_required
def add_to_watchlist(request, listing_id, listing_manipulation):

    listing = Listing.objects.get(pk=listing_id)
    if listing_manipulation == 'Add to watchlist':
        listing.watchlist.add(User.objects.get(pk=request.user.id))
        listing.save()
    elif listing_manipulation == 'Remove from watchlist':
        listing.watchlist.remove(User.objects.get(pk=request.user.id))
    else:
        listing.active = False
        max_bid_value = Bid.objects.filter(listing=listing_id).aggregate(Max('bid'))['bid__max']
        max_bid = Bid.objects.get(listing=listing, bid=max_bid_value)
        listing.winner = max_bid.user 
        listing.save()
    
    return HttpResponseRedirect(reverse('listing_page', args=(listing_id,)))


@login_required
@transaction.atomic # Setting up a transaction for the user to add to the Listing tabel and the initial bid to the Bid table. If either fails the other is not commited
# Create listing page which requires that user to be logged in
def create_listing(request):
    # When the user adds the listing
    if request.method == "POST":
        # Gather information from the Listing and Bid forms as well as store the user object
        listing_f = ListingForm(request.POST)
        bid_f = BidForm(request.POST)
        category_f = CategoryForm(request.POST)
        user = User.objects.get(pk=request.user.id)

        # Verify that the forms are valid
        if listing_f.is_valid() and bid_f.is_valid():
            # Add information from the ListingForm then add the user
            new_listing = listing_f.save(commit=False)
            new_listing.seller = user

            if category_f.is_valid() and category_f.cleaned_data['name']:
                new_category, created = Category.objects.get_or_create(name=category_f.cleaned_data['name'])
                new_category.save()
                new_listing.category = new_category

            new_listing.save()

            # Add bid information to the listing
            new_bid = bid_f.save(commit=False)
            new_bid.listing = new_listing
            new_bid.user = user
            new_bid.save()

            # Redirect the user to the index page after a successful listing creation
            return HttpResponseRedirect(reverse('index'))
        else:
            # If the form is not valid render an error page mentioning that the listing could not be added
            return render(request, 'auctions/error.html')
    else:
        return render(request, 'auctions/create_listing.html', {
            'listing_form': ListingForm(),
            'bid_form': BidForm(),
            'category_form': CategoryForm()
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
