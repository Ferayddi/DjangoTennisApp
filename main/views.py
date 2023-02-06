from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from datetime import datetime, timedelta
from django.conf import settings
from .models import Sessions
import threading
from django.core.mail import EmailMessage


class EmailThread(threading.Thread):
  def __init__(self, email):
    self.email = email
    threading.Thread.__init__(self)

  def run(self):
    self.email.send()



def login_access_only():
        def decorator(view_function):
            @wraps(view_function)
            def _wrapped_view(request, *args, **kwargs):
                if "logged_in" in request.session:
                    return view_function(request, *args, **kwargs)
                else:
                    messages.add_message(request, messages.WARNING, 'You do not have permission for this action, please login')
                    return redirect('/login')
            return _wrapped_view
        return decorator

def admin_access_only():
        def decorator(view_function):
            @wraps(view_function)
            def _wrapped_view(request, *args, **kwargs):
                if "is_admin" in request.session:
                    return view_function(request, *args, **kwargs)
                else:
                    messages.add_message(request, messages.WARNING, 'You do not have permission for this action, please login')
                    return redirect('/login')
            return _wrapped_view
        return decorator

# Create your views here.
@login_access_only()
def home(request):
    dt = datetime.today()
    day_wanted = int(settings.WEEK_SESSION)   #Which day the sessions are is defined in the environment file
    daysDiff = (day_wanted - dt.weekday()) % 7  
    #date + datetime.timedelta(days=days)
    nextPractice = dt + timedelta(days=daysDiff)
    nextPracticeDate = nextPractice.date()
    context = { #PracticeDate
        "PracticeDate": nextPracticeDate,
        "session1_start": settings.SESSION1_START,
        "session2_start": settings.SESSION2_START,
        "is_admin": request.session["is_admin"]
    }
    return render(request, 'main.html', context)


def logout(request):
    request.session.flush()
    return redirect('/login')


@login_access_only()
def practice(request):
    dt = datetime.today()
    day_wanted = int(settings.WEEK_SESSION)   #Which day the sessions are is defined in the environment file
    daysDiff = (day_wanted - dt.weekday()) % 7  
    nextPractice = dt + timedelta(days=daysDiff)
    nextPracticeDate = nextPractice.date()


    #Now gonna check if user has already signed up, if yes then add flash message
    query = Sessions.objects.filter(member_email= request.session['email'], date= nextPracticeDate)
    session_choice = request.POST["session_select"]
    if query.count() == 0:
        joining_student = Sessions(date= nextPracticeDate, member_email = request.session['email'], session_choice = session_choice)
        joining_student.save()
        messages.add_message(request, messages.SUCCESS, 'You have succesfully requested a spot for this week session, a confirmation email will be sent to you later')
        return redirect(home)
    else:
        messages.add_message(request, messages.WARNING, 'You have already signed up for this week practice, session ' + str(query[0].session_choice))
        return redirect(home)

@admin_access_only()   #try to nest decorator here
def confirmSessions(request):
    dt = datetime.today()
    day_wanted = int(settings.WEEK_SESSION)   #Which day the sessions are is defined in the environment file
    daysDiff = (day_wanted - dt.weekday()) % 7  
    nextPractice = dt + timedelta(days=daysDiff)
    nextPracticeDate = nextPractice.date()

    #retrieve records by asceding added int
    students_array = Sessions.objects.filter(date = nextPracticeDate).order_by('id')
    #sort them in respective sessions, based on environment capacity for the sessions
    session1_capacity = int(settings.SESSION1_CAPACITY)
    session2_capacity = int(settings.SESSION2_CAPACITY)

    for student in students_array:
        if student.session_choice == 1:
            if session1_capacity > 0:
                student.session_assigned = 1
                session1_capacity -= 1
                student.save()
            elif session2_capacity > 0 and student.session_flexible == 1:
                student.session_assigned = 2
                session2_capacity -= 1
                student.save()

        if student.session_choice == 2:
            if session2_capacity > 0:
                student.session_assigned = 2
                session2_capacity -= 1
                student.save()
            elif session1_capacity > 0 and student.session_flexible == 1:
                student.session_assigned = 1
                session1_capacity -= 1
                student.save()

    messages.add_message(request, messages.SUCCESS, 'Sessions were successfully sorted, emails should be sent shortly')


    #send emails: 
  
    



    return redirect(home)

@login_access_only()
def cancelPracticeSignUp(request):
    dt = datetime.today()
    day_wanted = int(settings.WEEK_SESSION)   #Which day the sessions are is defined in the environment file
    daysDiff = (day_wanted - dt.weekday()) % 7  
    nextPractice = dt + timedelta(days=daysDiff)
    nextPracticeDate = nextPractice.date()

    query = Sessions.objects.filter(member_email=request.session['email'], date = nextPracticeDate)

    if query.count() != 0:
        query[0].delete()
        messages.add_message(request, messages.SUCCESS, 'your registration for next week session has been canceled.')
        return redirect(home)
    else:
        messages.add_message(request, messages.WARNING, 'you are not signed up for next week session.')
        return redirect(home)