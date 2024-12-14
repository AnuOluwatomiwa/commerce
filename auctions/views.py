from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse


from .models import User, ListingForm, AuctionListings, Bids, Comments

def categories(request):
    categories = AuctionListings.objects.values_list('category', flat=True).distinct()#As seen in python documentation
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_listings(request, category_name):
    listings = AuctionListings.objects.filter(category=category_name, is_active=True)
    return render(request, "auctions/category_listings.html", {
        "category_name": category_name,
        "listings": listings
    })
    
def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    user_watchlist = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": user_watchlist
    })

def listing_page(request, listing_id):
    listing = get_object_or_404(AuctionListings, id=listing_id)
    comments = Comments.objects.filter(auction_listing=listing)
    is_watchlisted = listing.watchlist.filter(id=request.user.id).exists() if request.user.is_authenticated else False

    if request.method == "POST":
        #Handling the add/removal from watchlist
        if "watchlist" in request.POST:
            if is_watchlisted:
                listing.watchlist.remove(request.user)
            else:
                listing.watchlist.add(request.user)
        # To handle the bidding
        elif "bid" in request.POST:
            bid_amount = float(request.POST["bid"])
            if bid_amount >= listing.starting_bid and bid_amount > listing.current_bid:
                Bids.objects.create(bid_amount=bid_amount, user=request.user, auction_listing=listing)
                listing.current_bid = bid_amount
                #Save
                listing.save()
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "comments": comments,
                    "is_watchlisted": is_watchlisted,
                    "error": "Bid must be higher than the current price and starting bid."
                })
        #Closing auction
        elif "close" in request.POST and listing.user == request.user:
            listing.is_active = False
            listing.save()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments,
        "is_watchlisted": is_watchlisted
    })

def forms_view(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        starting_bid = request.POST['starting_bid']
        image_url = request.POST.get('image_url', '')  
        category = request.POST.get('category', '')
        current_bid = starting_bid  

        
        if not title or not description or not starting_bid:
            return render(request, 'auctions/forms.html', {'message': 'Please fill in all required fields.'})

        try:
            starting_bid = float(starting_bid)  
        except ValueError:
            return render(request, 'auctions/forms.html', {'message': 'Invalid starting bid format.'})

        # Create and Save the listing
        listing = AuctionListings.objects.create(
            title=title,
            description=description,
            starting_bid=starting_bid,
            current_bid = current_bid,
            image_url=image_url,
            category=category,
            user=request.user,  
        )
        return HttpResponseRedirect(reverse("index")) 
    else:
        form = ListingForm()
        return render(request, "auctions/forms.html", {'form': form})

def index(request):
    active_listings = AuctionListings.objects.all()
    return render(request, "auctions/index.html", {
        "listings": active_listings
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
