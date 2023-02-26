from django.http import HttpResponse
from django.shortcuts import render
from app.models import UserProfile

# Create your views here.

def home(request):
    context_dict = {}
    context_dict['most_popular_items'] = [{}, {}, {}]
    context_dict['other_items'] = [{}, {}, {}, {}, {}, {}]

    return render(request, 'app/home.html', context=context_dict)

def search(request):
    return HttpResponse("Hello, This is a search page")

def login(request):
    return HttpResponse("Hello, This is a login page")