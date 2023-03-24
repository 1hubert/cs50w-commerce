from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


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

CATEGORY_CHOICES = (
        (CLOTH := 'CLOTHING', 'Clothing & Accessories'),
        (HEALTH := 'HEALTH', 'Health & Beauty'),
        (FIT := 'FITNESS', 'Fitness'),
        (JWLR := 'JEWELRY', 'Jewelry'),
        (PET := 'PET', 'Pet Supplies'),
        (MOB := 'MOBILE', 'Mobile Phones & Accessories'),
        (CAM := 'CAMERAS', 'Cameras & Photos')
    )

class AuctionListing(models.Model):
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    starting_price = models.IntegerField()
    photo = models.URLField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    users_watching = models.ManyToManyField(User, related_name='users_watching', default=None, blank=True)

    def __str__(self) -> str:
        return f'listing: {self.title} by {self.user}'

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.value}$ bid by user {self.user} on listing {self.listing}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    body = models.CharField(max_length=500)

    def __str__(self) -> str:
        return f'{self.user}: {self.body}'
