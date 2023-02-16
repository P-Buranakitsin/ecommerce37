from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    context_dict = {}

    return render(request, 'app/home.html', context=context_dict)

def search(request):
    return HttpResponse("Hello, This is a search page")

def login(request):
    return HttpResponse("Hello, This is a login page")