from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .models import Tasks
from .forms import Task_form
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import redirect
    
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.forms import AuthenticationForm


# eamil varification
from rest_framework.authtoken.models import Token
# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User

# send user name 
def priority_filter(request, priority=None):
    without_filter_data = Tasks.objects.all()

    form = Task_form()
    if priority is not None:
        data = Tasks.objects.filter(priority = priority)
        # print( "slug",priority,'data', data)
        return render(request,'show_task.html',{'form':form,'object_list':data,'data':without_filter_data})
    if request.method == 'POST':
        form = Task_form(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save(commit=True)
            print("from pri :", form.cleaned_data)
             # sending email
            message =f'Task Created'
            send_email = EmailMultiAlternatives('Task','',to=[request.user.email])
            send_email.attach_alternative(message, 'text/html')
            send_email.send()

    data = Tasks.objects.all()
    print( "slug",priority,'data', data)
    return render(request,'show_task.html',{'form':form,'object_list':data,'user':request.user,'data':without_filter_data})

def status_filter(request, current_status=None):
    without_filter_data = Tasks.objects.all()

    form = Task_form()
    if current_status is not None:
        data = Tasks.objects.filter(current_status = current_status)
        print( "slug",current_status,'data', data)
        return render(request,'show_task.html',{'form':form,'object_list':data,'data':without_filter_data})
    if request.method == 'POST':
        form = Task_form(request.POST)
        if form.is_valid():
            form.save(commit=False)
            print("from pri :", form.cleaned_data)
             # sending email
            message =f'Task Created'
            send_email = EmailMultiAlternatives('Task','',to=[request.user.email])
            send_email.attach_alternative(message, 'text/html')
            send_email.send()

    data = Tasks.objects.all()
    print( "slug",current_status,'data', data)
    return render(request,'show_task.html',{'form':form,'object_list':data})

def due_date_filter(request, due_date=None):
    without_filter_data = Tasks.objects.all()

    form = Task_form()
    if due_date is not None:
        data = Tasks.objects.filter(due_date = due_date)
        print( "slug",due_date,'data', data)
        return render(request,'show_task.html',{'form':form,'object_list':data,'data':without_filter_data})
    if request.method == 'POST':
        form = Task_form(request.POST)
        if form.is_valid():
            form.save(commit=False)
            print("from pri :", form.cleaned_data)
             # sending email
            message =f'Task Created'
            send_email = EmailMultiAlternatives('Task','',to=[request.user.email])
            send_email.attach_alternative(message, 'text/html')
            send_email.send()

    data = Tasks.objects.all()
    print( "slug",due_date,'data', data)
    return render(request,'show_task.html',{'form':form,'object_list':data,'data':without_filter_data})

def edit_task(request, id):
    post = Tasks.objects.get(pk=id) 
    data = Tasks.objects.all()

    task_form = Task_form(instance=post)
    if request.method == 'POST':
        task_form = Task_form(request.POST, instance=post)
        if task_form.is_valid(): 
            task_form.save()
             # sending email
            message =f'Task Modified'
            send_email = EmailMultiAlternatives('Task','',to=[request.user.email])
            send_email.attach_alternative(message, 'text/html')
            send_email.send()
    return render(request,'show_task.html',{'form':task_form,'object_list':data})

def delete_task(request, id):
    post = Tasks.objects.get(pk=id) 
    post.delete()
    return redirect('home')



# register 
def task_maker_register(request):
    if request.method == 'POST':
        form =RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            print("uid :", uid)
            print("token :", token)
            confirm_link = f"http://127.0.0.1:8000/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return HttpResponse("Check your mail for confirmation")
    else:
        form = RegisterForm()
    return render(request, 'authientication.html',{'form': form})

# activate
def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode() 
        user =User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active =True
        user.save()
        return redirect('task_maker_login')
    else:
        return redirect('task_maker_register')
    

# login
def task_maker_login(request):
    if request.method =='POST':
        form =AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            name =form.cleaned_data['username']
            userpass =form.cleaned_data['password']
            user = authenticate(username=name, password=userpass)
            if user is not None:
                login(request, user)
                return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'authientication.html', {'form': form})

# logout
def task_maker_logout(request):
    logout(request)
    return redirect('home')
