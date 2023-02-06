from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('logout', views.logout, name='logout'),
    path('practice', views.practice, name="practice"),
    path('confirmSessions', views.confirmSessions, name="confirmSessions"),
    path('cancelPracticeSignUp', views.cancelPracticeSignUp, name="cancelPracticeSignUp")
]
