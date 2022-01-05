from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:item>", views.item, name="item"),
    path("watchlist/<str:user>", views.watchlist, name="watchlist"),
    path("cars", views.cars, name="cars"),
    path("others", views.others, name="others"),
    path("phones", views.phones, name="phones")
]
