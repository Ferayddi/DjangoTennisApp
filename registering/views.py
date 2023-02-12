from django.http import HttpResponse
from django.template import loader
from .models import Member
from .forms import MemberForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str,  DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from django.contrib import messages


class EmailThread(threading.Thread):

  def __init__(self, email):
    self.email = email
    threading.Thread.__init__(self)

  def run(self):
    self.email.send()


def send_activation_email(user, request):
    currrent_site = get_current_site(request)
    email_subject = 'Activate your tennis account'
    email_body = render_to_string('authentication/activate.html', {
      'user': user.english_name,
      'domain': currrent_site,
      'uid': urlsafe_base64_encode(force_bytes(user.email)),
      'token': generate_token.make_token(user)
    })


    email = EmailMessage(subject=email_subject, body= email_body, 
                from_email=settings.EMAIL_FROM_USER,
                to = [user.email])
    EmailThread(email).start()
    


# Create your views here.
def register(request):
    if request.method == 'GET':
        template = loader.get_template('registrationPage.html')
        context = {
        
        }
        return HttpResponse(template.render(context, request))
        



def signUp(request):
    context = {}
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
           if form.cleaned_data["email"].find('@ust.hk') ==-1 and form.cleaned_data["email"].find('@connect.ust.hk') ==-1:
              messages.add_message(request, messages.WARNING, 'Please use your school email')
              return render(request, 'registrationPage.html', context)
           if  form.cleaned_data["password1"] == form.cleaned_data["password2"]: # check if id or email is already in database
                if (Member.objects.filter(email = form.cleaned_data["email"]).count() != 0):
                  messages.add_message(request,messages.WARNING, 'Email is already being used')
                  return render(request, 'registrationPage.html', context)
                context = {
                  "email": form.cleaned_data["email"],
                }
                hashedpassword = make_password(form.cleaned_data["password1"])
                member = Member(english_name = form.cleaned_data["english_name"] , chinese_name = form.cleaned_data["chinese_name"],
                email = form.cleaned_data["email"] , password = hashedpassword, student_id = form.cleaned_data["student_id"])
                member.is_active = False
                member.save()
                send_activation_email(member, request)
                return render(request, 'thankyou.html', context)

        # else: since it didn't get returned
        template = loader.get_template('registrationPage.html')  
        messages.add_message(request, messages.WARNING, "There are errors in the form, please try again")
        return HttpResponse(template.render(context, request))

        


def activate_user(request, uidb64, token):
  uid= force_str(urlsafe_base64_decode(uidb64))
  user = Member.objects.filter(email=uid)[0]
  if (user != None) and (generate_token.check_token(user, token) == True):
    context = {}
    user.is_active = True
    user.save()
    messages.add_message(request, messages.SUCCESS, 'Email verified, you can now login')
    context = {}
    return redirect('/login')
  else:   ##IMPORTANT; FIX THIS ---------------------------------------------------------------------------------------------------------------------
    messages.add_message(request, messages.SUCCESS, 'Email verified, you can now login')
    return redirect('/login')
    


def sendAgain(request):
  
  verificationEmail = request.POST.get("verificationEmail")
  context = {
    "email": verificationEmail
  }
  print(verificationEmail)
  user = Member.objects.get(email= verificationEmail)
  if user:
    send_activation_email(user, request)
    return render(request, 'thankyou.html', context)
  else:
    messages.add_message(request, messages.WARNING, 'the email you inserted is not correct')
    return redirect('/login')