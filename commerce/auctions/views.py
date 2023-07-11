from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListing, WatchList, Bid, Winner, Comment, Category


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": AuctionListing.objects.filter(l_status=True),
        "c_auctions": AuctionListing.objects.filter(l_status=False),
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


@login_required
def create_listing(request):
    if request.method == "POST":
        lform = request.POST

        if not lform["l_price"] or not lform["l_title"] or not lform["l_description"]:
            return render(request, "auctions/create_listing.html", {
                "msg": "You must fill all required fields."
            })

        try:
            category = Category.objects.get(id=lform["l_category"])
        except ObjectDoesNotExist:
            category = Category.objects.get(name="Other")

        listing = AuctionListing(
            l_title=lform["l_title"],
            l_price=lform["l_price"],
            l_description=lform["l_description"],
            l_imglink=lform["l_imgurl"],
            l_category=category,
            l_user=request.user
        )

        listing.save()

        return render(request, "auctions/create_listing.html", {
            "msg": AuctionListing.objects.last()
        })

    return render(request, "auctions/create_listing.html",{
        "categories": Category.objects.all()
    })


def item(request, id):
    bid_msg = None
    try:
        auction_item = AuctionListing.objects.get(id=id)
        if auction_item.l_status == False:
            winner = Winner.objects.get(item=auction_item)
            if winner.user == request.user and winner.user == auction_item.l_user:
                bid_msg = "You closed this auction without any bids."
            elif winner.user == request.user:
                bid_msg = "You won this auction!"
    except ObjectDoesNotExist:
        auction_item = None

    # Handling post requests
    if request.method=="POST":

        # In case a bidder sent the request, update the price
        if request.POST["btn_type"] == "bidder":
            bid_price = float(request.POST["bid_price"])
            item_price = float(auction_item.l_price)

            if bid_price <= item_price:
                bid_msg = "Invalid price."

            else:
                auction_item.l_price = bid_price
                auction_item.save()
                bid = Bid(item=auction_item, user=request.user)
                bid.save()

        # In case the creater of the bid sent the request, close the auction
        elif request.POST["btn_type"] == "creator" and auction_item.l_status:
            last_bid = Bid.objects.filter(item=auction_item).last()
            if last_bid:
                winner = Winner(item=auction_item, user=last_bid.user)
                winner.save()
            else:
                winner = Winner(item=auction_item, user=auction_item.l_user)
                winner.save()
            auction_item.l_status = False
            auction_item.save()

        # In case the request is a comment, post the comment
        elif request.POST["btn_type"] == "comment":
            comment = request.POST["comment"]
            new_comment = Comment(item=auction_item, user=request.user, comment=comment)
            new_comment.save()

    # WatchList verifications
    try:
        wl = WatchList.objects.get(item=auction_item, user=request.user)
        wl_msg = "Remove from Watchlist"
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        wl_msg = "Add to Watchlist"
    except TypeError:
        wl_msg = None

    # Getting number of bids
    nbids = Bid.objects.filter(item=auction_item).count()
    if auction_item:
        if auction_item.l_status and bid_msg != "Invalid price.":
            bid_msg = f"{nbids} bid(s) so far."
            last_bid = Bid.objects.filter(item=auction_item).last()
            if last_bid and request.user==last_bid.user:
                bid_msg = bid_msg + " Your bid is the current bid."

    # Get request
    return render(request, "auctions/item.html", {
        "auction": auction_item,
        "wl_msg": wl_msg,
        "bid_msg": bid_msg,
        "comments": Comment.objects.filter(item=auction_item),
        "nbids": nbids,
    })


@login_required
def watchlist(request):

    # Adding to or removing of watchlist
    if request.method=="POST":
        item_id = request.POST
        auction_item = AuctionListing.objects.get(id=item_id["wl"])
        try:
            wl = WatchList.objects.get(item=auction_item, user=request.user)
            wl.delete()
        except ObjectDoesNotExist:
            wl = WatchList(item=auction_item, user=request.user)
            wl.save()
        except MultipleObjectsReturned:
            ...
        return redirect("item", id=item_id["wl"])

    return render(request, "auctions/watchlist.html", {
        "auctions": WatchList.objects.filter(user=request.user)
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def category(request, id):
    this_category = Category.objects.get(id=id)
    itens = this_category.categories.filter(l_status=True)
    return render(request, "auctions/category.html", {
        "category": this_category,
        "itens": itens,
    })