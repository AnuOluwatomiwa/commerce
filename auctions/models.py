from django import forms
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class ListingForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    starting_bid = forms.DecimalField(max_digits=10, decimal_places=2)
    image_url = forms.URLField(required=False)
    category = forms.ChoiceField(choices=[
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'),
        ('Home', 'Home'),
    ], required=False)


class AuctionListings(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    # Set default to None to allow for initial "python3 manage.py makemigrations"
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    watchlist = models.ManyToManyField(User, related_name="watchlist", blank=True)

    @property
    def highest_bidder(self):
        highest_bid = self.bids.order_by('-bid_amount').first()
        return highest_bid.user if highest_bid else None


class Bids(models.Model):
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)