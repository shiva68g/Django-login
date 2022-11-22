from django.urls import path 
from .views import *
urlpatterns = [
    path('register' , register , name='register'),
    path('login' ,  loginuser , name='login'),
    path('otp' , verifyotp , name = 'verifyotp'),
    path(''  , home , name="home"),
    path('logout', userlogout , name="logout")
]