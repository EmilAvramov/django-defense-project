from django.shortcuts import render

def home(request):
    return render(request, 'main/pages/home.html', {})

def about(request):
    return render(request, 'main/pages/about.html', {})