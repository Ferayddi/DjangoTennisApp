from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),   #renders  the '' path
    path('logout', views.logout, name='logout'),   # occurs when logout button is clicked
    path('practice', views.practice, name="practice"),   # occurs when people register for a session
    path('confirmSessions', views.confirmSessions, name="confirmSessions"),   # Occurs when admin click on "confirm Session"
    path('cancelPracticeSignUp', views.cancelPracticeSignUp, name="cancelPracticeSignUp"),   #Occurs when someone clicks on "canecel Registration"
    path('manageSessions', views.manageSessions, name="manageSessions"),    # Occurs when an admin clicks on "manage sessions"
    path('processAttendance/<id>', views.processAttendance, name="processAttendance"),    #Occurs when an admin click on a name, in the "manageSessions.html" template
    path('processPayment', views.processPayment, name= "processPayment")   #occurs when  someone submit the submit button in the manage session template
]
