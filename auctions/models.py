from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import datetime



class User(AbstractUser):
    pass


class Auction(models.Model):
    CATEGORY = (
        ("others", "OTHERS"),
        ("cars", "CARS"),
        ("phones", "Phones")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ownerOf")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    link = models.URLField(blank=True)
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    category = models.CharField(max_length=12, choices=CATEGORY, default='Others')
    

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        exclude = ["active", "user"]



class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Auction, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["price"]


class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, default=" ")

class CommentForm(ModelForm):
    class Meta:
        fields = ["comment"]


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    