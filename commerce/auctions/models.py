from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class AuctionListing(models.Model):
    l_title = models.CharField(max_length=64)
    l_price = models.DecimalField(max_digits=14,decimal_places=2)
    l_description = models.CharField(max_length=512)
    l_imglink = models.URLField()
    l_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories", default="Other")
    l_timestamp = models.DateTimeField(auto_now_add=True)
    l_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctioneers")
    l_status = models.BooleanField(default=True)

    def __str__(self):
        return f"Auction {self.id}: {self.l_title} at {self.l_timestamp}"


class Winner(models.Model):
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="winner1")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner2")
    timestamp = models.DateTimeField(auto_now_add=True)


class WatchList(models.Model):
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchlisted")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")


class Bid(models.Model):
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bid1")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid2")
    timestamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comment1")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment2")
    comment = models.CharField(max_length=256, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)

