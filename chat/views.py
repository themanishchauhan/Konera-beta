from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from chat.models import Thread
from chat.models import ChatMessage
from accounts.models import Profile

@login_required
def users(request): 
    fp = Profile.objects.get(user = request.user)
    threads = Thread.objects.by_user(profile=fp).order_by('-timestamp')  
    

    try:
        if request.method == 'POST':
            secondP = request.POST.get('secondP')
            secondPuser_obj = User.objects.get(username=secondP)
            SecondPprofile = Profile.objects.get(user = secondPuser_obj)
            chat_obj = Thread.objects.filter(first_person = fp,second_person=SecondPprofile) | Thread.objects.filter(first_person = SecondPprofile,second_person=fp)
            if chat_obj:
                messages.success(request, 'Already a Friend.')
                return redirect('users')
            else:
                thread_obj = Thread.objects.create(first_person =fp, second_person = SecondPprofile)
                thread_obj.save()
                messages.success(request, 'Already a Friend.')
                return redirect('users')
    except Exception as e:
            print(e)
    
    chat_list = []
    for thread in threads:
        try:
            chat = ChatMessage.objects.filter(thread=thread).latest('date').message
            if chat == None:
                chat_list.append('start chat...')
            else:
                chat_list.append(chat)
        except:
            pass
    
    context = {
        'Threads':threads,
        'chats':chat_list,
        'Me':fp
    }
    return render(request, 'chat/users.html', context)

# @login_required 
# def messages_page(request,thread_id):
#     # threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
#     threads = Thread.objects.get(id=thread_id) #.prefetch_related('chatmessage_thread').order_by('timestamp')
#     print(thread_id)
#     context = {
#         'thread': threads
#     }
#     return render(request, 'messages.html', context)

@login_required
def getmessages(request,thread):
    all_messages=ChatMessage.objects.all().filter(thread=thread)
    return JsonResponse({"messages":list(all_messages.values())})


@login_required
def chat (request,thread):
    threads = Thread.objects.get(id=thread)
    fp = Profile.objects.get(user = request.user)

    if threads.first_person == fp: 
        # name = threads.second_person.username
        # user_obj = User.objects.get(username=name)
        profile_obj= threads.second_person
    else: 
        # name = threads.first_person.username
        # user_obj = User.objects.get(username=name)
        profile_obj= threads.first_person

    all_messages=ChatMessage.objects.all().filter(thread=thread)
    all_messages_count = all_messages.count()
    print(thread,all_messages_count)
    print(thread)
    context = {
        'user':fp,
        'thread': threads,
        'profile': profile_obj,
        'count':all_messages_count
    }
    return render(request, 'chat/messages.html', context)

@login_required
def send(request):
    if request.user.is_anonymous or request.user.is_active==False:
        return redirect('/accounts/login')
    if request.method == 'POST':
        sender= Profile.objects.get(user = request.user)
        thread_id=request.POST.get("friend")  
        message=request.POST.get("message")
        message=message.strip()
        thread = Thread.objects.get(pk=thread_id)
        if (message == "") or (Profile.objects.get(user = request.user) != sender):
            return redirect(f'/chat/{thread_id}')
        newmessage=ChatMessage(sender=sender,thread=thread,message=message)
        newmessage.save()
        thread.timestamp = datetime.now()
        thread.save()
        return HttpResponse("message sent")

    # return redirect('/')
    # if(request.method=='POST'):
    #     user= request.user.username
    #     # thread_id = thread
    #     thread_id = Thread.objects.get(pk=thread)
    #     print(thread_id,message,user)
    #     new_message= ChatMessage(sender=user,thread=thread_id,message=message)
    #     new_message.save()


    
    # return HttpResponse('File uploaded successfully!')

def search_address(request):
    user = request.GET.get('user')
    payload = []
    if user:
        user_obj = User.objects.filter(username__icontains = user)
        for i in user_obj:
            Profile_objs = Profile.objects.filter(name__icontains=i)
            for obj in Profile_objs:
                payload.append(obj.user.username)
        


    return JsonResponse({'status' : 200 , 'data' : payload})