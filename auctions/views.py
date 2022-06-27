from asyncio.windows_events import NULL
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
import datetime
from annoying.functions import get_object_or_None
from django.contrib.auth.decorators import login_required

from .models import User,Listing,Watchlist,UserBid,UserComment

def index(request):
    return render(request, "auctions/index.html",{
        "items" : Listing.objects.filter(sold=False),
    })
    
@login_required
def sold(request):
    return render(request, "auctions/sold.html",{
        "items" : Listing.objects.filter(sold=True),
    })

@login_required
def create(request):
    if request.method == "POST":
        listing = Listing()
        listing.sold = False
        listing.title = request.POST.get("title").strip()
        listing.seller = request.user.username
        listing.description = request.POST.get("description").strip()
        if listing.title == "" or listing.description == "" or request.POST.get("price").isdigit()==False:
            return render(request, "auctions/create.html", {"message": "Can't save with empty field."})
        else:
            if request.POST.get("image_link")==False:
                listing.image_link = "https://www.aust-biosearch.com.au/wp-content/themes/titan/images/noimage.gif"
            else:
                listing.image_link = request.POST.get("image_link")
            if request.POST.get("category"):
                listing.category = request.POST.get("category").strip()
            listing.price = int(request.POST.get("price"))
            listing.save()
            return render(request, "auctions/index.html",{
                "items" : Listing.objects.all(),
            })
    return render(request,"auctions/create.html",{
        "listings" : Listing.objects.all(),
    })
 
@login_required   
def listing(request,id):
    added = Watchlist.objects.filter(listing_id=id)
    listing = Listing.objects.get(pk=id)
    if listing.sold == True and request.user.username == listing.winner:
        is_winner = True
        return render(request, "auctions/sold.html",{
            "items" : Listing.objects.filter(sold=True),
            "is_winner" : is_winner,
            "listing":listing
        })
    elif listing.sold == True and request.user.username == listing.seller:
        seller = True
        return render(request, "auctions/sold.html",{
            "items" : Listing.objects.filter(sold=True),
            "seller" : seller,
            "listing":listing
        })
    elif listing.sold == True and request.user.username != listing.seller and request.user.username != listing.winner:
        other = True
        return render(request, "auctions/sold.html",{
            "items" : Listing.objects.filter(sold=True),
            "other" : other,
            "listing":listing
        })
            
    is_owner = True if listing.seller == request.user.username else False
    if request.method == "POST":
        comment = request.POST.get('comment', None)
        
        if comment:
            c = UserComment.objects.create(content = comment, user = request.user.username, listing_id = listing.id)
            c.save()
        else:
            c = None
        bid = request.POST.get('b', False)
        if int(bid) > listing.price:
            listing.price = bid
            listing.save()
            bidobj = UserBid.objects.filter(listing_id=id)
            if bidobj:
                bidobj.delete()
            bid_user = UserBid()
            bid_user.listing_id = listing.id
            bid_user.user_bid = bid
            bid_user.user =  request.user.username
            bid_user.save()
            return render(request,"auctions/listing.html",{
            "listing": listing,
            "added":added,
            "message": "Your Bid is added.",
            "msg_type": "success",
            "is_owner":is_owner,
            "comments":UserComment.objects.all()})   
        elif int(bid) == False:
            return render(request,"auctions/listing.html",{
            "listing": listing,
            "added":added,
            "message": "",
            "msg_type": "danger",
            "is_owner":is_owner,
            "comments":UserComment.objects.all()})  
        elif int(bid) <= listing.price:
            return render(request,"auctions/listing.html",{
            "listing": listing,
            "added":added,
            "message": "Your Bid should be higher than the Current one.",
            "msg_type": "danger",
            "is_owner":is_owner,
            "comments":UserComment.objects.all()})    
    return render(request,"auctions/listing.html",{
        "listing": Listing.objects.get(pk=id),
        "added":added,
        "is_owner":is_owner,
        "comments":UserComment.objects.all()})

@login_required   
def close_bidding(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    is_owner = True if listing.seller == request.user.username else False
    if is_owner:
        listing.winner = UserBid.objects.get(user_bid = listing.price).user
        listing.sold = True
        listing.save()
 
    return render(request, "auctions/close_bidding.html", {
        "listing": listing,
        "is_owner": is_owner,
    })    

@login_required   
def categories(request):
    return render(request,"auctions/categories.html")

@login_required
def category(request, categ):
    # retieving all the products that fall into this category
    categ_products = Listing.objects.filter(category=categ)
    empty = False
    if len(categ_products) == 0:
        empty = True
    return render(request, "auctions/category.html", {
        "categ": categ,
        "empty": empty,
        "products": categ_products
    })
    
@login_required
def watchlist(request,id):
    obj = Watchlist.objects.filter(listing_id=id)
    if obj:
        obj.delete()
        listing = Listing.objects.get(pk=id)
        added = Watchlist.objects.filter(listing_id=id)
        return render(request,"auctions/listing.html",{
        "listing": listing,
        "added" :  added
    })
    else:
        obj = Watchlist()
        obj.listing_id = id
        obj.save()
        listing = Listing.objects.get(pk=id)
        added = Watchlist.objects.filter(listing_id=id)
        return render(request,"auctions/listing.html",{
            "listing": listing,
            "added" :  added
    })
        
@login_required
def watchlistpage(request):
    return render(request, "auctions/watchlist.html",{
        "items" : Listing.objects.all(),
        "watchlistings" :Watchlist.objects.all()
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
    


    

