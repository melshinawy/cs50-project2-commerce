from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.create_listing, name="create_listing"),
    path('<int:listing_id>', views.listing_page, name="listing_page"),
    path('categories', views.categories, name='categories'),
    path('categories/<str:category_id>', views.category_name, name="category_name"),
    path('add_to_watchlist/<int:listing_id>/<str:listing_manipulation>', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist', views.watchlist, name='watchlist')
]
