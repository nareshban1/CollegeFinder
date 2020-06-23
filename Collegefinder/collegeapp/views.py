from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User,auth
from django.core.mail import send_mail, BadHeaderError
from .models import College,Course,Comment,Location
from .forms import *
from django.contrib import messages
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from sklearn.externals import joblib
from tensorflow.keras.models import load_model
from tensorflow.python.keras import backend as k
from django.db.models import Avg,Func

model= load_model(r'C:\Users\nares\sentiment.h5')
tokenizer= joblib.load(r'C:\Users\nares\tokenizer.pkl')

def index(request):
    obj = Course.objects.all()
    locn = Location.objects.all()
    college = College.objects.all().prefetch_related('courses', 'location')[:10]
    context = {
        'object': obj,
        'locn':locn,
        'college': college
    }
    return render(request,'index.html', context)


def is_valid_queryparam(param):
    return param != '' and param is not None



def colleges(request):
    obj=College.objects.all().prefetch_related('courses','location')
    coursesall = Course.objects.all()
    locall= Location.objects.all()
    coursefilter = request.GET.get('coursefilter')
    locationfilter = request.GET.get('locationfilter')

    if is_valid_queryparam(coursefilter) and coursefilter != 'Choose...':
        obj = obj.filter(courses__shortname = coursefilter)

    if is_valid_queryparam(locationfilter) and locationfilter != 'Choose...':
        obj = obj.filter(location__locationname = locationfilter)

    paginator = Paginator(obj, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if(coursefilter is not None and locationfilter is not None):
        if(coursefilter != 'Choose...' and locationfilter != 'Choose...'):
            cfilter = coursefilter + ' Colleges in ' + locationfilter
        elif (coursefilter != 'Choose...' and locationfilter == 'Choose...'):
            cfilter = coursefilter + ' Colleges'
        elif (coursefilter == 'Choose...' and locationfilter != 'Choose...'):
            cfilter = ' Colleges in ' + locationfilter
        else:
            cfilter = ''
    else:
        cfilter=''


    context ={
        'name':cfilter,
        'object': page_obj,
        'coursesall': coursesall,
        'locall': locall

    }
    return render(request,'Acollege.html', context)


def details(request, id):
    college= College.objects.get(id=id)
    comments = Comment.objects.filter(college=college).order_by('-id')

    class Round(Func):
        function = 'ROUND'
        arity = 2

    all = []
    Rating = []
    if(comments.count() >0 ):
        rating= comments.aggregate(rounded_avg = Round(Avg('rating'),0))
        rate= int(rating['rounded_avg'])

        for i in range(0, rate):
            Rating.append(i)

        for i in range(0, 5 - rate):
            all.append(i)

    is_favourite = False
    if college.favourite.filter(id=request.user.id).exists():
        is_favourite= True

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            comment = request.POST.get('comment')
            txt = comment
            seq = tokenizer.texts_to_sequences([txt])
            padded = pad_sequences(seq, maxlen=50)
            #pred = model.predict_classes(padded)
            score = model.predict(padded)
            if (score > 0.60 and score < 0.75):
                rating=4
            elif (score > 0.75):
                rating=5
            elif (score > 0.49 and score < 0.59):
                rating=3
            elif (score < 0.49 and score > 0.25):
                rating=2
            else:
                rating=1
            comm= Comment.objects.create(college=college, rating=rating, user= request.user, comment=comment)
            comm.save()
            comment_form = CommentForm()
            return HttpResponseRedirect('/details/(%s)/' %id)
    else:
        comment_form = CommentForm()
    context = {
        'object': college,
        'comments': comments,
        'rating': Rating,
        'all': all,
        'is_favourite': is_favourite,
        'comment_form': comment_form
    }
    return render(request,'cdetails.html',context)


def course_college(request, id):
    course= Course.objects.get(id=id).courses.all()
    paginator = Paginator(course, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cname = Course.objects.get(id=id).shortname + ' Colleges'
    context = {
        'name': cname,
        'object': page_obj
    }
    return render(request,'colleges.html',context)

def location(request, id):
    loca= Location.objects.get(id=id).location.all()
    paginator = Paginator(loca, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    locname='Colleges in  ' +Location.objects.get(id=id).locationname
    context = {
        'name':locname,
        'object': page_obj
    }
    return render(request,'colleges.html',context)

def search(request):
    query = request.GET.get('q')
    obj = College.objects.all().prefetch_related('courses', 'location')
    results = obj.filter(Q(collegename__icontains=query))
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cname = 'Colleges with similar names to '+query
    context = {
        'name': cname,

        'object': page_obj
    }
    return render(request,'colleges.html',context)


def favourite(request, id):
    college = get_object_or_404(College, id=id)
    if college.favourite.filter(id=request.user.id).exists():
        college.favourite.remove(request.user)
    else:
        college.favourite.add(request.user)
    return HttpResponseRedirect('/details/(%s)/' %id)

def favourite_list(request):
    user = request.user
    favourites = user.favourite.all()
    paginator = Paginator(favourites, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    name = 'Your Favourites'
    context = {
        'name': name,
        'object': page_obj
    }
    return render(request, 'colleges.html', context)

def contact(request):
    if request.method == 'GET':
        contact_form = ContactForm()
    else:
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            subject = contact_form.cleaned_data['subject']
            name= contact_form.cleaned_data['name']
            email = contact_form.cleaned_data['email']
            message = contact_form.cleaned_data['message']
            contact_message = "%s: %s" % (
                name,
                message,
                )
            try:
                send_mail( subject= subject, message= contact_message, from_email= email , recipient_list= ['naresh.herald@gmail.com'], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, 'Message sent')
    return render(request, 'contactus.html', {'contact_form': contact_form})




