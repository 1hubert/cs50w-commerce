from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
        starting_price = int(request.POST['starting_price'])
        image_url = request.POST['image_url']
        category = request.POST['category']

        # Attempt to create a new listing
        listing = AuctionListing(
            title=title,
            description=description,
            starting_price=starting_price,
            photo=image_url,
            user=request.user,
            category=category
        )
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

        bids = Bid.objects.filter(listing=listing.id)
        if bids:
            listing.price = bids.aggregate(
                Max('value')
            )['value__max']
            listing.highest_bidder = bids.filter(
                value=listing.price
            )[0].user
            listing.bid_count = bids.count()
        else:
            listing.price = listing.starting_price
            listing.bid_count = 0

        comments = Comment.objects.filter(listing=listing.id)

        return render(request, 'auctions/listing.html', {
            "listing": listing,
            "watchlisted": watchlisted,
            "comments": comments
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
    listing = get_object_or_404(AuctionListing, id=listing_id)
    if request.method == 'POST' and listing.active == True:
        bid_requested = int(request.POST['bid'])
        user_id = request.user.id
        bids = Bid.objects.filter(listing_id=listing_id)

        if bids:
            max_bid = bids.aggregate(Max('value'))['value__max']
            print(max_bid)

            # If the bid  requested is too low, return to the last-viewed page
            if bid_requested <= max_bid:
                messages.error(request, 'Your bid must be higher than the highest bid!', extra_tags='danger')
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            starting_price = get_object_or_404(
                AuctionListing,
                id=listing_id
            ).starting_price

            # If the bid  requested is too low, return to the last-viewed page
            if bid_requested <= starting_price:
                messages.error(request, 'Your bid must be higher than the starting price!', extra_tags='danger')
                return HttpResponseRedirect(request.META['HTTP_REFERER'])


        # The new bid must be greater than starting price (if no bids) or the highest bid
        # Create a new bid
        # return HttpResponse(f'starting price is {starting_price}$ / bid requested is {bid_requested}$')
        user = get_object_or_404(User, id=user_id)
        new_bid = Bid(value=bid_requested, user=user, listing=listing)
        new_bid.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect(reverse('index'))


def close_listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    listing.active = False
    listing.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(
        AuctionListing,
        id=listing_id
    )
    if request.method == 'POST':
        comment = request.POST['comment']
        user = request.user
        new_comment = Comment(
            body=comment,
            user=user,
            listing=listing
        )
        new_comment.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect(reverse('index'))


def categories(request):
    return render(request, 'auctions/all_categories.html', {
        "category_choices": CATEGORY_CHOICES
    })


def listings_by_category(request, category):
    return render(request, 'auctions/listings_by_category.html', {
        "listings": AuctionListing.objects.filter(category=category),
        "category": [choice[1] for choice in CATEGORY_CHOICES if choice[0] == category][0]
    })
