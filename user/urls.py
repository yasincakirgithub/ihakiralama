from django.urls import path
from user.views import *

urlpatterns = [
    path('login/', loginPage, name='loginPage'),
    path('logout/', logoutPage, name='logoutPage'),
    path('register/', registerPage, name='registerPage'),
]