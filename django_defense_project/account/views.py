from django.shortcuts import render

def register(request):
    return render(request, 'account/public/register.html', {})

def login(request):
    return render(request, 'account/public/login.html', {})

def profile(request):
    return render(request, 'account/protected/profile.html', {})