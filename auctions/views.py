from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import AuctionForm, Auction, Bid, Comment, Watchlist
from django.contrib.auth.decorators import login_required
from .models import User


def index(request):
    auctions = Auction.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "auctions": auctions
    })

def cars(request):
    auctions = Auction.objects.filter(category="cars", active=True)
    return render(request, "auctions/cars.html", {
        "auctions": auctions
    })

def others(request):
    auctions = Auction.objects.filter(category="others", active=True)
    return render(request, "auctions/others.html", {
        "auctions": auctions
    })

def phones(request):
    auctions = Auction.objects.filter(category="phones", active=True)
    return render(request, "auctions/phones.html", {
        "auctions": auctions
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
        if password  == "":
            return render(request, "auctions/register.html", {
                "message": "Passwords must not be empty."
            })
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

def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "form": AuctionForm
        })
    if request.method == "POST":
        user = request.user
        owner_item = Auction(user=user) 
        form = AuctionForm(request.POST, instance=owner_item)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("create")
        else:
            print(form.errors.as_data())
            return render(request, "auctions/create.html", {
                "message" : "description limit is 450 characters"
            })

@login_required
def item(request, item):
    if request.method == "GET":
        highest_bid = Bid.objects.filter(item=item).order_by('price').last()
        user = request.user
        winner = highest_bid
        product = Auction.objects.get(id=item)
        bid = Bid.objects.filter(item=item).order_by('-price')[:3] 
        comments = Comment.objects.filter(auction=item)
        # Check if item is on watchlist
        watchlist = Watchlist.objects.filter(auction=item, user=request.user)
        return render(request, "auctions/item.html", {
            "auction": product,
            "bids": bid,
            "comments": comments,
            "watchlist": watchlist,
            "winner": winner,
            "user": user
        })

    if request.method == "POST":
        current_item = Auction.objects.get(id=item)
        current_user = request.user

        # BID SECTION
        # Make first bid
        if request.POST.get('price'):        
            highest_bid = Bid.objects.filter(item=item).order_by('price').last()
            new_bid = request.POST.get('price')
            if new_bid is not None:
                if highest_bid is None:
                    if float(new_bid) > current_item.start_price:
                        add_bid = Bid(user=current_user, item=current_item, price=float(new_bid))
                        add_bid.save()

                # Other bids
                else:
                    price_highest_bid = highest_bid.price 
                    if float(new_bid) > price_highest_bid:
                        add_bid = Bid(user=current_user, item=current_item, price=float(new_bid))
                        add_bid.save()
   
        # Close auction and assign winner
        product = Auction.objects.get(id=item)
        if request.POST.get('close_auction'):
            if product.active == 1:
                # Check highest bid
                highest_bid = Bid.objects.filter(item=item).order_by('price').last()
                if highest_bid is None:
                    current_item.active = False
                    current_item.save()
                    return HttpResponseRedirect(reverse('item', args=[item]))
                if current_item.start_price < highest_bid.price:
                    current_item.active = False
                    current_item.save()   
                    return HttpResponseRedirect(reverse('item', args=[item]))
        

            # COMMENT SECTION 
        if request.POST.get('comment'):
            # comment_title = request.POST.get('title')
            comment = request.POST.get('comment')
            if comment is not None:
                add_comment = Comment(user=current_user, auction=current_item, comment=comment)
                add_comment.save()


        # WATCHLIST SECTION
        # ADD to watchlist
        watchlist = Watchlist.objects.filter(auction=current_item, user=current_user)
        if request.POST.get('on_watchlist'):
            if not watchlist:
                on_watchlist = Watchlist(auction=current_item, user=current_user)
                on_watchlist.save()
            else:
                off_watchlist = watchlist
                off_watchlist.delete()

        return HttpResponseRedirect(reverse("item", args=[item]))


def watchlist(request, user):
    if request.method == "GET":
        # Get the items from the watchlist
        user = User.objects.get(username=user)
        user_id = user.id
        watchlist = Watchlist.objects.filter(user=user_id).values_list('auction', flat=True)
        items = Auction.objects.filter(id__in=watchlist)
        return render(request, "auctions/watchlist.html", {
            "items": items
        })
