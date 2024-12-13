from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("form", views.forms_view, name="form"),
    path("listing/<int:listing_id>", views.listing_page, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]