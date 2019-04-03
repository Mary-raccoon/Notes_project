from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
from django.core import serializers
from django.http import JsonResponse


def login(request):
    errors = User.objects.login_validator(request.POST)
    
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags="login")
        return redirect('/')
    
    user = User.objects.get(email=request.POST['email1'])
    
    if bcrypt.checkpw(request.POST['password1'].encode(), user.password.encode()):
        print("password match")
        request.session['id'] = user.id
        request.session['name'] = user.name
        request.session['email'] = user.email
        messages.success(request, "You successfully logged in")
        return redirect('/notes')
    else:
        print("wrong password")
        return redirect('/')
    print(user.name)

   
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for field, msg in errors.items():
            messages.error(request, msg, extra_tags=field)
        return redirect('/')
    else:
        hash_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print(hash_password)
        user = User.objects.create(
            name=request.POST['name'],  
            email=request.POST['email'],
            password=hash_password
        )
        request.session['name'] = user.name
        messages.success(request, "User successfully created")
        return redirect('/notes')


def logout(request):
    request.session.flush()
    return redirect('/')


def log_reg(request):
    return render(request, 'notes/log_reg.html')


def notes(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        'user': User.objects.get(id=request.session['id']),
        'notes': Note.objects.all()
    }
    print("request.session id: ", request.session['id'])
    return render(request, 'notes/notes.html', context)


def post_note(request):
    errors = Note.objects.note_validator(request.POST)
    if len(errors):
        for key, msg in errors.items():
            messages.error(request, msg, extra_tags=key)
        return redirect('/notes')
    else:
        note = Note.objects.create(
            label=request.POST['label'],
            desc=request.POST['desc'],
            author_id=request.session['id']
        )
        request.session['label'] = note.label
        messages.success(request, "Note successfully created")
        return redirect('/notes')


def read(request, id):
    context = {
        'note': Note.objects.get(id=id)
    }
    return render(request, 'notes/view.html', context)


def edit(request, id):
    context = {
        'note': Note.objects.get(id=id)
    }
    return render(request, 'notes/edit.html', context)


def update(request, id):
    errors = Note.objects.note_validator(request.POST)
    if len(errors):
        for key, msg in errors.items():
            messages.error(request, msg, extra_tags=key)
        return redirect('/'+id+'/edit')
    else:
        if request.method == "POST":
            print("*"*20)
            up_note = Note.objects.get(id=id)
            up_note.label = request.POST['label']
            up_note.desc = request.POST['desc']
            up_note.save()
            
            return redirect('/notes')


def destroy(request, id):
    Note.objects.get(id=id).delete()
    print('cancel ', id)
    return redirect('/notes')


def api(request):
    return render(request, 'notes/api.html')


def all_json(request):
    data = {
        "users": User
    }
    users = User.objects.all()
    return HttpResponse(serializers.serialize("json", users), content_type='application/json')
    # return JsonResponse(data)


def all_notes(request):
    notes = Note.objects.all()
    return HttpResponse(serializers.serialize("json", notes), content_type='application/json')


def red_notes(request):
    red = Note.objects.filter(label__icontains="red") 
    return HttpResponse(serializers.serialize("json", red), content_type='application/json')


def yellow_notes(request):
    yellow = Note.objects.filter(label__icontains="yellow") 
    return HttpResponse(serializers.serialize("json", yellow), content_type='application/json')


def blue_notes(request):
    blue = Note.objects.filter(label__icontains="blue") 
    return HttpResponse(serializers.serialize("json", blue), content_type='application/json')


def green_notes(request):
    green = Note.objects.filter(label__icontains="green") 
    return HttpResponse(serializers.serialize("json", green), content_type='application/json')
