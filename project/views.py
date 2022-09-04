from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout

def home(request):
    logout(request)
    return render(request, 'home.html')

def base(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'home.html', context)