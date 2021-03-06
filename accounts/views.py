from django.http.response import HttpResponse
from accounts.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.core import mail
# Create your views here.


def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/accounts/login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/accounts/login')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/accounts/login')
        
        login(request , user)
        return redirect('/')

    return render(request , 'accounts/login.html')

def register_attempt(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        profile_pic = request.FILES.get('image')
        ano = request.POST.get('ano')
        date_of_exam = request.POST.get('date_of_exam')
        your_address = request.POST.get('your_address')
        exam_centre = request.POST.get('venue')

        print(password)

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                # return redirect('/register')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                # return redirect('/register')
            
            if Profile.objects.filter(ano = ano).first():
                messages.success(request, 'Application already exists')
                # return redirect('/register')
            user_obj = User.objects.create(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token,name = name, ano = ano,date_of_exam = date_of_exam, your_address = your_address, exam_centre = exam_centre,profile_pic =profile_pic)
            profile_obj.save()
            send_mail_after_registration(email , auth_token, name, username)
            return redirect('/token')

        except Exception as e:
            print(e)


    return render(request , 'accounts/register.html')

def success(request):
    return render(request , 'accounts/success.html')


def token_send(request):
    return render(request , 'accounts/token_send.html')



def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/accounts/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'accounts/error.html')


def ChangePassword(request , token):
    try:
        profile_obj = Profile.objects.filter(auth_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('password1')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')  
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/')
            
    except Exception as e:
        print(e)
    return render(request , 'accounts/change-password.html' , context)

def ForgetPassword(request):

    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            
            if not User.objects.filter(username=username).first():
                messages.success(request, 'No user found with this username.')
                return redirect('/')
            print(username)
            user_obj = User.objects.get(username = username)
            profile_obj= Profile.objects.get(user = user_obj)
            print(profile_obj)
            token = profile_obj.auth_token
            print(user_obj.email)
            print(token)
            Send_forget_password_mail(user_obj.email,token,username)
            print('hii')
            messages.success(request, 'An email is sent.')
            print('sucess')
            return redirect('/')
                
    except Exception as e:
        print(e)
    return render(request , 'accounts/forget-password.html')





def send_mail_after_registration(email , token, name, username):
    subject = f'{name}, Activate Your Account!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    context = {
        'name': name,
        'username':username,
        'token':token,
    }
    html_message = render_to_string('email/activate_account.html',context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message , email_from ,recipient_list,html_message=html_message)

def Send_forget_password_mail(email,token,username):
    subject = 'Reset Password!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email] 
    context = {
        'username':username,
        'token':token,
    }
    html_message = render_to_string('email/forget_password.html',context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message , email_from ,recipient_list,html_message=html_message)


def Check(request):
    name = 'Manish Chauhan'
    token = 'www.facebook.com'
    email = 'manishchouhan770@gmail.com'
    username = 'manishchauhan'
    send_mail_after_registration(email , token, name, username)
    return HttpResponse('Sent')


def forget(request):
    # name = 'Manish Chauhan'
    token = 'www.instagram.com'
    email = 'manishchouhan770@gmail.com'
    username = 'manishchauhan'
    Send_forget_password_mail(email , token,username)
    return HttpResponse('Sent')

