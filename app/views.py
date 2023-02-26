from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app.models import UserProfile
from app.forms import CreateUserForm
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

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        form = authenticate(request, username=username, password=password)

        if form is not None:
            login(request, form)
            return redirect('home')

        else:
            messages.info(request, "Username or Password is incorrect!")

    context = {}
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

#ShoppingCart
@login_required
def viewShoppingCart(request):
    return 0

@login_required
def addShoppingCart(request):
    return 0

@login_required
def removeShoppingCart(request):
    return 0