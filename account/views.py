from django.shortcuts import render
from django.contrib import auth
from .forms import LoginForm, RegisterForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/show/')
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.logout(request)
                auth.login(request, user)
                return HttpResponseRedirect('/')
        else:
            return render(request, 'login.html', {'message': list(login_form.errors.values())[0][0]})
    else:
        return render(request, 'login.html')

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
        return HttpResponseRedirect('/login/')

    return HttpResponseRedirect('/login/')


def register(request):
    if request.user.is_authenticated():
        auth.logout(request)
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            User.objects.create_user(username=username, password=password, email=email)
            return HttpResponseRedirect('/login/')
        else:
            return render(request, 'register.html', {'message': list(register_form.errors.values())[0][0]})

    else:
        return render(request, 'register.html')

