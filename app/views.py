from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from app.models import UserProfile
from app.forms import CreateUserForm, LoginUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    context_dict = {}
    context_dict['most_popular_items'] = [{}, {}, {}]
    context_dict['other_items'] = [{}, {}, {}, {}, {}, {}]

    return render(request, 'app/home.html', context=context_dict)

def search(request):
    return HttpResponse("Hello, This is a search page")

class LoginView(View):
    def get(self, request):
        form = LoginUserForm()
        context = { 'form': form}
        return render(request, 'app/login.html',context)

    def post(self, request):
        form = LoginUserForm(request.POST)

        if form.is_valid():
            login(request, form)
            return redirect(reverse('app:home'))
        else:
            print(form.errors)

        context = { 'form': form}
        return render(request, 'app/login.html',context)
        
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account was created for " + user)
            return redirect('login')
            #return HttpResponse('1')
    else:
        context = {'form': form}
    return render(request, 'app/register.html', context)
    #return HttpResponse('2')

def test(request):
    return HttpResponse('Homepage')

def logout(request):
    logout(request)
    return redirect('home')

def buy(request):
    print(123123123)
    form = CreateUserForm()
    context = {'form': form}
    return render(request, 'app/buy.html', context)