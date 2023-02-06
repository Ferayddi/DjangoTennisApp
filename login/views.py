from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.hashers import check_password
from registering.models import Member
from django.shortcuts import redirect, render
from django.urls import clear_url_caches
from django.contrib import messages

# Create your views here.



def login(request, *args, **kwargs):
    context = {}
    template = loader.get_template('login.html')
    return HttpResponse(template.render(context, request))


def signIn(request):
    context = {}
    email = request.POST["email"]
    password = request.POST["password"]
    mydata = Member.objects.filter(email = email).values()
    if mydata.count() != 0:
        myuser = mydata[0]
        checked = check_password(password, myuser["password"])
    else:
        messages.add_message(request, messages.WARNING, 'Invalid email or Password')
        return render(request, 'login.html', context)


    if myuser["is_active"] == False:
        messages.add_message(request, messages.WARNING, """You must validate your email first """, 'email')  
        return redirect("/login")


    if checked == True: 
        #render to homescreen
        request.session['email'] = email
        request.session['logged_in'] = True
        request.session['is_admin'] = myuser["is_admin"]
        return redirect('/')
    else:
        messages.add_message(request, messages.WARNING, 'Invalid email or Password')
        
    return render(request, 'login.html', context)