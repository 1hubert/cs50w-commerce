from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_listing, name="new_listing"),
    path("show/<int:listing_id>", views.show_listing, name="show_listing"),
    path("show/watchlist/<int:listing_id>", views.watchlist_add, name="watchlist_add"),
    path("watchlist", views.watchlist, name="watchlist"),
]
