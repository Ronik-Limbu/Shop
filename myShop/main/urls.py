from django.urls import path
from .views import *

urlpatterns = [
    path("",index,name="index"),
    path("blog_single/",blog_single,name="blog_single"),
    path("blog/",blog,name="blog"),
    path("cart/",cart_detail,name="cart"),
    path("checkout/",checkout,name="checkout"),
    path("contact/",contact_us,name="contact_us"),
    path("product_detail/<int:id>",product_detail,name="product_detail"),
    path("shop/",shop,name="shop"),
    path("login.html/",log_in,name="log_in"),
    path("register/",register,name="register"),
    path("profile/",customer_profile,name="profile"),

    path('cart/add/<int:id>/',cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'), 
    path('cart/cart-detail/',cart_detail,name='cart_detail'),
]
