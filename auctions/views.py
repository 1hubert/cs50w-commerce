from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, AuctionListing, Bid, Comment
from .models import CATEGORY_CHOICES


def index(request):
    listings = AuctionListing.objects.all()
    for listing in listings:
        bids = Bid.objects.filter(listing=listing.id)
        if bids:
            listing.price = bids.aggregate(
                Max('value')
            )['value__max']
        else:
            listing.price = listing.starting_price
    return render(request, "auctions/index.html", {
        "listings": listings
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


def new_listing(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        starting_bid = int(request.POST['starting_bid'])
        image_url = request.POST['image_url']
        category = request.POST['category']

        # Attempt to create a new listing
        listing = AuctionListing(title=title, description=description, starting_bid=starting_bid, photo=image_url, user=request.user, category=category)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'auctions/new_listing.html', {
            "category_choices": CATEGORY_CHOICES
        })


def show_listing(request, listing_id):
    if request.method == 'POST':
        pass

    else:
        listing = get_object_or_404(AuctionListing, id=listing_id)
        watchlisted = listing.users_watching.filter(id=request.user.id).exists()

        return render(request, 'auctions/listing.html', {
            "listing": AuctionListing.objects.get(id=listing_id),
            "watchlisted": watchlisted,
            "max_bid": Bid.objects.filter(listing=listing_id).aggregate(Max('value'))['value__max']
        })


def watchlist_add(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    if listing.users_watching.filter(id=request.user.id).exists():
        listing.users_watching.remove(request.user)
    else:
        listing.users_watching.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "listings": AuctionListing.objects.filter(users_watching=request.user)
    })

def place_bid(request, listing_id):
    if request.method == 'POST':
        bid_requested = int(request.POST['bid'])
        user_id = request.user.id
        bids = Bid.objects.filter(listing_id=listing_id)

        if bids:
            max_bid = bids.aggregate(Max('value'))['value__max']
            print(max_bid)

            # If the bid  requested is too low, return to the last-viewed page
            if bid_requested <= max_bid:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            starting_price = get_object_or_404(
                AuctionListing,
                id=listing_id
            ).starting_price

            # If the bid  requested is too low, return to the last-viewed page
            if bid_requested <= starting_price:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])


        # The new bid must be greater than starting price (if no bids) or the highest bid
        # Create a new bid
        # return HttpResponse(f'starting price is {starting_price}$ / bid requested is {bid_requested}$')
        user = get_object_or_404(User, id=user_id)
        listing = get_object_or_404(AuctionListing, id=listing_id)
        new_bid = Bid(value=bid_requested, user=user, listing=listing)
        new_bid.save()
        print(new_bid)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect(reverse('index'))
