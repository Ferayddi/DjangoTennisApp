from . import views
from django.urls import path

urlpatterns = [
    path('', views.register, name="register"),
    path('signUp', views.signUp, name="signUp"),
    path('activate-user/<uidb64>/<token>', views.activate_user, name="activate"), #receiving token from email
    path('activation', views.sendAgain, name="activation")

]