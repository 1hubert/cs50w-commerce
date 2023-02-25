from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# You will also need to add additional models to this file to represent details about (3 required, 1 optional):
# auction listings
# bids
# comments
# auction categories (model is optional, category functionality is required)

# Remember that each time you change anything in auctions/models.py, you’ll need to first run:
# 1) python manage.py makemigrations 
# 2) python manage.py migrate 
# to migrate those changes to your database

class AuctionListing(models.Model):
    CATEGORY_CHOICES = (
        (CLOTH := 'CLOTHING', 'Clothing & Accessories'),
        (HEALTH := 'HEALTH', 'Health & Beauty'),
        (FIT := 'FITNESS', 'Fitness'),
        (JWLR := 'JEWELRY', 'Jewelry'),
        (PET := 'PET', 'Pet Supplies'),
        (MOB := 'MOBILE', 'Mobile Phones & Accessories'),
        (CAM := 'CAMERAS', 'Cameras & Photos')
    )
    
    user_id = models.IntegerField()
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    starting_bid = models.IntegerField()
    photo = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

class Bid(models.Model):
    user_id = models.IntegerField()
    listing_id = models.IntegerField()
    value = models.IntegerField()

class Comment(models.Model):
    user_id = models.IntegerField()
    listing_id = models.IntegerField()
    body = models.CharField(max_length=500)
    