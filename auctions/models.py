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