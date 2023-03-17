from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from app.models import UserProfile, ShoppingCart, Commodities
from app.forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm

# Create your views here.

def home(request):
    print(User.objects.all())
    context_dict = {}
    context_dict['most_popular_items'] = [0, 1, 2]
    context_dict['other_items'] = [0, 1, 2, 3, 4, 5]

    return render(request, 'app/home.html', context=context_dict)

class SearchView(View):
    def get(self, request):
        items = []
        for i in range(12):
            items.append(i)

        default_page = 1
        page = request.GET.get('page', default_page)

        # Paginate items
        items_per_page = 9
        paginator = Paginator(items, items_per_page)
        try:
            items_page = paginator.page(page)
        except PageNotAnInteger:
            items_page = paginator.page(default_page)
        except EmptyPage:
            items_page = paginator.page(paginator.num_pages)

        context_dict = { 'items_page': items_page}
        return render(request, 'app/search.html', context=context_dict)
    
class UserLoginView(View):
    def get(self, request):
        form = AuthenticationForm(request)
        context = { 'form': form}
        return render(request, 'app/login.html',context)

    def post(self, request):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('app:home'))
        else:
            print(form.errors)

        context = { 'form': form}
        return render(request, 'app/login.html',context)
    
class CommodityView(View):
    def get(self, request, c_id):
        print(c_id)
        context_dict={}
        context_dict['related_items'] = [0, 1, 2]
        context_dict['c_id'] = c_id

        return render(request, 'app/commodity.html', context=context_dict)
    
    def post(self, request, c_id):
        print(request.POST.get('inputQuantity'))
        context_dict={}
        context_dict['related_items'] = [0, 1, 2]

        return render(request, 'app/commodity.html', context=context_dict)
    
class ContactUsView(View):
    def get(self, request):
        context_dict={}
        return render(request, 'app/contactUs.html', context_dict)
    
class CartView(View):
    def get(self, request):
        context_dict={}
        context_dict['cart_items'] = [0, 1, 2]
        return render(request, 'app/cart.html', context_dict)

class ProfileView(View):
    def get_user_details(self):
        return

    def get(self, request):
        items = []
        for i in range(3):
            items.append(i)

        default_page = 1
        page = request.GET.get('page', default_page)

        # Paginate items
        items_per_page = 999
        paginator = Paginator(items, items_per_page)
        try:
            items_page = paginator.page(page)
        except PageNotAnInteger:
            items_page = paginator.page(default_page)
        except EmptyPage:
            items_page = paginator.page(paginator.num_pages)

        form = PasswordChangeForm(request.user)
        context_dict = {'form': form, 'items_page': items_page}
        
        return render(request, 'app/profile.html', context_dict)
    
    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save(commit=False)
        else:
            print(form.errors)

        context_dict = {'form' : form}
        
        return render(request, 'app/profile.html', context_dict)

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
# @login_required
# def viewShoppingCart(request):
#     items = ShoppingCart.objects.filter(user = request.user)
#     price = 0
#     for item in items:
#         price += item.commodities.price * ShoppingCart.amount
#         context = {
#             'items': items,
#             'price': price
#         }
#     return render(request, 'users/cart.html', context)
#     #return HttpResponse('1')

@login_required
def addShoppingCart(request, c_id):
    c = Commodities.objects.get(c_id = c_id)
    shoppingCart, created = ShoppingCart.objects.get_or_create(
        user=request.user,
        commodities=c,
        defaults={'amount': 1}
    )
    if not created:
        shoppingCart.quantity += 1
        shoppingCart.save()
    return redirect('')

@login_required
def removeShoppingCart(request, c_id):
    '''
    shoppingCart = request.session.get('cart', {})
    ShoppingCart.remove()
    '''
    shoppingCart = ShoppingCart(request)
    commodities = get_object_or_404(Commodities, c_id=c_id)
    shoppingCart.remove(commodities)
    return redirect('cart')