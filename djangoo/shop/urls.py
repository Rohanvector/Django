from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('registor/',views.reg,name='reg'),
    path('collections/',views.col,name='col'),
    path('collections/<str:name>',views.colv,name='colv'),
    path('collections/<str:cname>/<str:pname>',views.prod,name='prod'),
    path('login',views.login_page,name="login_page"),
    path('logout',views.logout_page,name="logout_page"),
    path('addtocart',views.add_to_cart,name="addtocart"),
    path('cart',views.cart_page,name="cart"),
    path('remove_cart/<str:cid>',views.remove_cart,name="remove_cart"),
    path('favourite',views.fav_page,name="fav_page"),
    path('addtofav',views.add_to_fav,name="addtocart"),
    path('remove_fav/<str:fid>',views.remove_fav,name="remove_fav")
]