from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/",views.create,name="create"),
    path("listing/<int:id>",views.listing,name="listing"),
    path("categories/",views.categories,name="categories"),
    path("category/<str:categ>", views.category, name="category"),
    path("watchlist/<int:id>",views.watchlist,name="watchlist"),
    path("watchlist",views.watchlistpage,name="watchlistpage"),
    path("close_bidding/<int:listing_id>", views.close_bidding, name="close_bidding"),
    path("sold/",views.sold,name="sold")
]