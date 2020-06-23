from django.db.models import Q
from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User,auth
# Create your views here.
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email, first_name = first_name, last_name=last_name)
                user.save()
                print('created')
                messages.success(request, 'User created')
                return redirect('login')
        else:
            messages.warning(request, 'Passwords do not match')
            return redirect( 'register')
    else:
        return render(request,'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.warning(request, ' Login Failed! Enter the username and password correctly')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')