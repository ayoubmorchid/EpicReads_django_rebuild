from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

urlpatterns = [
    path("", views.home, name="home"),
    path("books/", views.book_list, name="book_list"),
    path("books/add/", views.book_create, name="book_create"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("books/<int:pk>/edit/", views.book_update, name="book_update"),
    path("books/<int:pk>/delete/", views.book_delete, name="book_delete"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("checkout/", views.checkout, name="checkout"),
    path("checkout/cart/<int:pk>/", views.cart_update, name="cart_update"),
    path("favorites/<int:pk>/toggle/", views.favorite_toggle, name="favorite_toggle"),
    path("payment/", views.payment, name="payment"),
    path("register/", views.register, name="register"),
    path("signup/", views.register, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="home"),
        name="logout",
    ),
]
