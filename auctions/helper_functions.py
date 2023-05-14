from .models import *
from django.db.models import Max
# Helper functions to be used throughout the project

# Returns a dictionary with listing as key and max_bid as value
def get_max_bids(listings):
    listings_max_bids = {}
    max_bids = Bid.objects.values('listing').annotate(Max('bid'))

    for listing in listings:
        listings_max_bids[listing] = max_bids.get(listing=listing)['bid__max']
    return listings_max_bids