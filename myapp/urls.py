"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('blog/',views.blog,name='blog'),
    path('contact/',views.contact,name='contact'),
    path('product/ <str:cat>/',views.product,name='product'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('fpass/',views.fpass,name='fpass'),
    path('otp/',views.otp,name='otp'),
    path('newpass/',views.newpass,name='newpass'),
    path('cpass/',views.cpass,name='cpass'),
    path('profile/',views.profile,name='profile'),
    path('sindex/',views.sindex,name='sindex'),
    path('add/',views.add,name='add'),
    path('view/',views.view,name='view'),
    path('pdetail/ <int:pk>/',views.pdetail,name='pdetail'),
    path('pedit/ <int:pk>/',views.pedit,name='pedit'),
    path('pdelete/ <int:pk>/',views.pdelete,name='pdelete'),
    path('bpdetail/ <int:pk>/',views.bpdetail,name='bpdetail'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('addtowishlist/ <int:pk>/',views.addtowishlist,name='addtowishlist'),
    path('deletetowishlist/ <int:pk>/',views.deletetowishlist,name='deletetowishlist'),
    path('shopping_cart/',views.shopping_cart,name='shopping_cart'),
    path('addtocart/ ',views.addtocart,name='addtocart'),
    path('deletetocart/ <int:pk>/',views.deletetocart,name='deletetocart'),
    path('changequantity/ <int:pk>/',views.changequantity,name='changequantity'),
    path('ajax/',views.ajax,name='ajax'),
    path('success/',views.success,name='success'),
    path('myorder/',views.myorder,name='myorder'),
    path('jssignup/',views.jssignup,name='jssignup'),
]