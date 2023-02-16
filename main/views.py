from django.shortcuts import render
from django.template.loader import render_to_string
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from datetime import datetime, timedelta
from django.conf import settings
from .models import Sessions
from registering.models import Member
import pytz




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
    dt = dt.astimezone(pytz.timezone('Hongkong'))       #NOT SURE ABOUT THIS
    currentHour = dt.astimezone(pytz.timezone('Hongkong')).strftime('%H')
    currentDay = dt.astimezone(pytz.timezone('Hongkong')).weekday()

    day_wanted = int(settings.WEEK_SESSION)   #Which day the sessions are is defined in the environment file
    daysDiff = (day_wanted - dt.weekday()) % 7  
    nextPractice = dt + timedelta(days=daysDiff)
    nextPracticeDate = nextPractice.date()

    student_info = Member.objects.filter(email= request.session["email"]).values()[0]
    membership_paid = "No" if (student_info["paid"] == False or student_info["paid"] == None) else "Yes"
    query = Sessions.objects.filter(member_email= request.session["email"]).values_list("session_choice")
    already_signed_up = query[0][0] if query.count() != 0 else '0'    #already signed up will be equal to session choice if exist, else 0
    # prevent people from cancelling after 6pm of the day before the practice, or prevent cancellation if day of practice
    close_registration = False if ((int(currentHour) >= 18 and int(currentDay) == settings.WEEK_SESSION - 1) or (int(currentDay) == settings.WEEK_SESSION)) else True 
    context = { #PracticeDate
        "close_registration": close_registration,
        "PracticeDate": nextPracticeDate,
        "session1_start": settings.SESSION1_START,
        "session2_start": settings.SESSION2_START,
        "is_admin": request.session["is_admin"],
        "email": student_info["email"],
        "english_name": student_info["english_name"],
        "student_id": student_info["student_id"],
        "membership_duration": student_info["membership_years_duration"],
        "membership_paid": membership_paid,
        "already_signed_up": already_signed_up,
    }
    return render(request, 'main.html', context)


def logout(request):
    request.session.flush()
    return redirect('/login')


@login_access_only()
def practice(request):
    dt = datetime.today()
    dt = dt.astimezone(pytz.timezone('Hongkong'))       #NOT SURE ABOUT THIS
    day_wanted = int(settings.WEEK_SESSION)   #Which day the sessions are is defined in the environment file
    daysDiff = (day_wanted - dt.weekday()) % 7  
    nextPractice = dt + timedelta(days=daysDiff)
    nextPracticeDate = nextPractice.date()


    #Now gonna check if user has already signed up, if yes then add flash message
    query = Sessions.objects.filter(member_email= request.session['email'], date= nextPracticeDate)
    session_choice = request.POST["session_select"]
    if query.count() == 0:
        foreign_member = Member.objects.get(email=request.session['email'])
        joining_student = Sessions(date= nextPracticeDate, member_email = foreign_member, session_choice = session_choice)
        if "session_flexible" in request.POST:
            joining_student.session_flexible = 1
        else:
            joining_student.session_flexible = 0

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


    #Set them all back to 0, so that we can re run if someone cancels, or just to make sure it is correct
    for student_temp in students_array:
        student_temp.session_assigned = 0
        student_temp.save()

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


    #change this so that we actually have the sessions instances, and hence can check in template if one has paid.
    session1_emails = Sessions.objects.filter(date = nextPracticeDate, session_assigned= "1" ).values_list('member_email', flat=True)
    session1_emails = list(session1_emails)

    session2_emails = Sessions.objects.filter(date = nextPracticeDate, session_assigned= "2" ).values_list('member_email', flat=True)
    session2_emails = list(session2_emails)

    no_sessions_emails = Sessions.objects.filter(date = nextPracticeDate, session_assigned= "0" ).values_list('member_email', flat=True)
    no_sessions_emails = list(no_sessions_emails)


    context = {
        "session1_emails":session1_emails,
        "session2_emails":session2_emails,
        "no_sessions_email": no_sessions_emails,
    }

    return render(request, 'confirmSessions.html', context)

@login_access_only()
def cancelPracticeSignUp(request):
    dt = datetime.today()
    dt = dt.astimezone(pytz.timezone('Hongkong'))       #NOT SURE ABOUT THIS
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

@admin_access_only()
def manageSessions(request):

    dt = datetime.today()
    dt = dt.astimezone(pytz.timezone('Hongkong'))       #NOT SURE ABOUT THIS
    day_wanted = int(settings.WEEK_SESSION)   #Which day the sessions are is defined in the environment file
    daysDiff = (day_wanted - dt.weekday()) % 7  
    nextPractice = dt + timedelta(days=daysDiff)
    nextPracticeDate = nextPractice.date()

    #change this so that we can actually choose the session
    session1_expected = Sessions.objects.filter(session_assigned = 1, attended = 0, date = nextPracticeDate)
    session1_attended = Sessions.objects.filter(session_assigned = 1,attended = 1, date = nextPracticeDate)
    
    session2_expected = Sessions.objects.filter(session_assigned = 2, attended = 0, date = nextPracticeDate)
    session2_attended = Sessions.objects.filter(session_assigned = 2, attended = 1, date = nextPracticeDate)

    all_sessions_students = Sessions.objects.filter(date = nextPracticeDate )

    context = {
        "all_sessions_students": all_sessions_students,
        "session1_expected": session1_expected,
        "session1_attended": session1_attended,
        "session2_expected": session2_expected,
        "session2_attended": session2_attended
    }
    return render(request, 'manageSessions.html', context)

@admin_access_only()
def processAttendance(request, id):

    dt = datetime.today()
    dt = dt.astimezone(pytz.timezone('Hongkong'))       #NOT SURE ABOUT THIS
    day_wanted = int(settings.WEEK_SESSION)   #Which day the sessions are is defined in the environment file
    daysDiff = (day_wanted - dt.weekday()) % 7  
    nextPractice = dt + timedelta(days=daysDiff)
    nextPracticeDate = nextPractice.date()


    query = Sessions.objects.filter(id = id, date = nextPracticeDate).all()

    if query.count() == 0: 
        messages.add_message(request, messages.WARNING, 'Student not found?' )
        return redirect(home)
    else:
        student = query[0]
    if student.attended== 0:
        student.attended=1
    else:
        student.attended=0

    student.save()
    return redirect(manageSessions)


def processPayment(request):
    if int(request.POST['membership_duration']) == 0:
        messages.add_message(request, messages.WARNING, 'Membership cannot be set to 0')
        return redirect(manageSessions)
    
    student = Member.objects.filter(email = request.POST['student_email'])

    if len(student) == 0:
        messages.add_message(request, messages.WARNING, 'Student not found')
        return redirect(manageSessions)
    
    student = student[0]

    student.paid = 1
    student.membership_years_duration = request.POST['membership_duration']
    student.save()
    messages.add_message(request, messages.SUCCESS, 'Payment processed succesfully')
    return redirect(manageSessions)

