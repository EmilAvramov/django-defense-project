from django.shortcuts import render

def register(request):
    return render(request, 'auth/register.html', {})

def login(request):
    return render(request, 'auth/login.html', {})

def guest(request):
    return render(request, 'auth/guest.html', {})