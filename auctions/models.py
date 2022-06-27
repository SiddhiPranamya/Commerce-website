from datetime import date, datetime
from sre_parse import CATEGORIES
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files import File
from django import forms

CATEGORY = (
    ('FASHION','Fashion'),
    ( 'ELECTRONICS','Electronics'),
    ('BEAUTY','Beauty'),
    ('BOOKS','Books'),
    ('VEHICLES','Vehicles'),
    ('KITCHENWARE','Kitchenware'),
    ('HEALTHCARE','Healthcare'),
    ('KIDS','Kids'),
    ('GARDENING','Gardening'),
    ('HYGINE','Hygine'),
    ('GROCERY','Grocery'),
    ('GENERAL','General')
)

class User(AbstractUser):
    pass

class Listing(models.Model):
    seller = models.CharField(max_length=64)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    image_link = models.CharField(max_length=200, default=None, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY, default='GENERAL')
    sold = models.BooleanField(default=False)
    winner = models.CharField(max_length=64)
    def __str__(self):
        return f" {self.title} - {self.description} {self.price}"
    
class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listing_id = models.IntegerField()
    
class UserBid(models.Model):
    user_bid = models.IntegerField()
    listing_id = models.IntegerField()
    title = models.CharField(max_length=64)
    user = models.CharField(max_length=64)
    def __str__(self):
        return f" {self.title} - {self.user_bid} {self.user}"
    
class UserComment(models.Model):
    content = models.TextField()
    user = models.CharField(max_length=64)
    listing_id = models.IntegerField()
    

