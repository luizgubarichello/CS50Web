from django.contrib import admin

from .models import User, AuctionListing, WatchList, Bid, Winner, Comment, Category
# Register your models here.
admin.site.register(User)
admin.site.register(AuctionListing)
admin.site.register(WatchList)
admin.site.register(Bid)
admin.site.register(Winner)
admin.site.register(Comment)
admin.site.register(Category)