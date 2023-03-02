from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from app.models import UserProfile, ShoppingCart, Commodities
from app.forms import CreateUserForm, LoginUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def home(request):
    context_dict = {}
    context_dict['most_popular_items'] = [{}, {}, {}]
    context_dict['other_items'] = [{}, {}, {}, {}, {}, {}]

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

#ShoppingCart
@login_required
def viewShoppingCart(request):
    items = ShoppingCart.objects.filter(user = request.user)
    price = 0
    for item in items:
        price += item.commodities.price * ShoppingCart.amount
        context = {
            'items': items,
            'price': price
        }
    return render(request, 'users/cart.html', context)
    #return HttpResponse('1')

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