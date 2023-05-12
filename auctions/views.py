from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import *
from .models import *


def index(request):
    # Create QuerySets for the active listings and maximum bid 
    active_listings = Listing.objects.exclude(active=False).all()
    max_bids = Bid.objects.values('listing').annotate(Max('bid'))

    # Create a dict to map active listings with highest bid
    listings_max_bids = {}

    for listing in active_listings:
        listings_max_bids[listing] = max_bids.get(listing=listing)['bid__max']

    return render(request, "auctions/index.html",{
        'listings': listings_max_bids
    })

def categories(request):
    categories_list = Listing.objects.exclude(category__isnull=True).values('category').distinct()
    return render(request, "auctions/categories.html", {
        'categories': categories_list
    })

def category_name(request, category):
    pass

def listing_page(request, listing_id):
    if request.method == 'GET':
        user_id = request.user.id
        context = {
            'listing': Listing.objects.get(pk=listing_id),
            'max_bid': Bid.objects.filter(listing=listing_id).aggregate(Max('bid'))['bid__max'],
            'user_id': user_id
        }

        if user_id:
            context['bid_form'] = BidForm()

    return render(request, "auctions/listing_page.html", context)

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
            new_listing.user = user

            if category_f.is_valid():
                new_category = category_f.save(commit=False)
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
