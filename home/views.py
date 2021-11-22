from typing import Text
from django.core.checks import messages
from django.shortcuts import render, redirect
from accounts.models import Profile
from django.http import HttpResponse
from django.contrib.auth import logout
from chat.models import Thread 
from .models import Feedback
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

 
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def home (request):
    posts = Profile.objects.all()
    pcount = posts.count()
    print(pcount)
    context ={
        'posts': posts,
        'count':pcount
        }
    # try:
    #     if request.method == 'POST':
    #         first_person = request.user
    #         print(first_person)
    #         second_person = posts.user
    #         print(second_person)
    #         chat_obj = Thread.objects.filter(first_person = first_person,second_person=second_person).first()
    #         if chat_obj:
    #             return redirect('users')
    #         else:
    #             thread_obj = Thread.objects.create(first_person =first_person, second_person = second_person)
    #             thread_obj.save()
    #             return redirect('users')
    # except Exception as e:
    #         print(e)
    return render(request, 'home/home.html', context)


@login_required
def post(request, ano): 
    posts = Profile.objects.get(ano=ano)
    fp = Profile.objects.get(user = request.user)
    chat_obj = Thread.objects.filter(first_person = fp,second_person=posts) | Thread.objects.filter(first_person = posts,second_person=fp)
    try:
        if request.method == 'POST':
            print(fp)
            print(posts)
            if chat_obj:
                return redirect('users')
            else:
                thread_obj = Thread.objects.create(first_person =fp, second_person = posts)
                thread_obj.save()
                return redirect('users')
    except Exception as e:
            print(e)
    context = {
        'posts': posts,
        'fp':fp,
        'exist':chat_obj,
        }
    return render(request, 'home/profile.html', context)


@login_required
def feedback_view(request):
    if request.method == 'POST':
        user = Profile.objects.get(user = request.user)
        feedback = request.POST.get('feedback')
        feedback_obj = Feedback.objects.create(user = user,text = feedback)
        feedback_obj.save()
        messages.success(request, 'Feedback has successfully submitted')
    return render(request,'home/feedback.html')