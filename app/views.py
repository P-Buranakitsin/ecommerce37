from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from app.models import UserProfile, CartItem, Commodities, Type, Purchase
from app.forms import UserRegisterForm, UserProfileForm
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.utils.decorators import method_decorator
import json

# Create your views here.
class HomeView(View):
    def get(self, request):
        popular_commodities = Commodities.objects.filter(type__name='Bag')
        other_commodities = Commodities.objects.filter(Q(type__name='Clothing') | Q(type__name='Fruit'))
        context_dict = {}
        context_dict['most_popular_items'] = popular_commodities
        context_dict['other_items'] = other_commodities
        return render(request, 'app/home.html', context=context_dict)

class SearchView(View):
    def get(self, request):
        query = request.GET.get('item_name')
        if (query is None):
            items = Commodities.objects.all()
        else:
            items = Commodities.objects.filter(c_name__icontains=query)

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
    
class UserRegisterView(View):
    def get(self, request):
        user_form = UserRegisterForm()
        profile_form = UserProfileForm()
        context = {'user_form': user_form, 'profile_form': profile_form}
        return render(request, 'app/register.html', context)
    
    def post(self, request):
        user_form = UserRegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(request.POST.get('password1'))
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            return redirect(reverse('app:home'))
        else:
            print(user_form.errors, profile_form.errors)       

        context = {'user_form': user_form, 'profile_form': profile_form}
        return render(request, 'app/register.html', context)

    
class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('app:home'))
    
class CommodityView(View):
    def get(self, request, c_id):
        selected_commodity = Commodities.objects.get(c_id=c_id)
        related_items = Commodities.objects.order_by('?')[:3]
        context_dict={}
        context_dict['related_items'] = related_items
        context_dict['selected_item'] = selected_commodity

        return render(request, 'app/commodity.html', context=context_dict)
    
class ContactUsView(View):
    def get(self, request):
        context_dict={}
        return render(request, 'app/contactUs.html', context_dict)
    
class CartView(View):
    @method_decorator(login_required(login_url=reverse_lazy('app:login')))
    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.sub_total_price for item in cart_items)
        context_dict={}
        context_dict['cart_items'] = cart_items
        context_dict['total_price'] = total_price
        return render(request, 'app/cart.html', context_dict)

class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'picture': user_profile.picture})
        
        return (user, user_profile, form)
    
    def paginate_user_purchases(self, request, username):
        items = Purchase.objects.filter(user=request.user)

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

        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))
        return (items_page, user_profile, user)

    @method_decorator(login_required(login_url=reverse_lazy('app:login')))
    def get(self, request, username):
        (items_page, user_profile, user) = self.paginate_user_purchases(request, username)
        form = PasswordChangeForm(request.user)
        context_dict = {'form': form, 'items_page': items_page, 'user_profile': user_profile, 'selected_user': user, 'active_tab': 'profile'}    
        return render(request, 'app/profile.html', context_dict)
    
    @method_decorator(login_required(login_url=reverse_lazy('app:login')))
    def post(self, request, username):
        (items_page, user_profile, user) = self.paginate_user_purchases(request, username)
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect(reverse('app:home'))
        else:
            print(form.errors)
        
        context_dict = {'form': form, 'items_page': items_page, 'user_profile': user_profile, 'selected_user': user, 'active_tab': 'security'}
        return render(request, 'app/profile.html',context_dict)

class AddtoCartView(View):
    @method_decorator(login_required(login_url=reverse_lazy('app:login')))
    def get(self, request, *args, **kwargs):
        return
    
    @method_decorator(login_required(login_url=reverse_lazy('app:login')))
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'authenticated': False})
        
        c_id = int(request.POST.get('c_id'))
        amount = int(request.POST.get('amount'))
        commodity = get_object_or_404(Commodities, c_id=c_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, commodities=commodity)

        if created:
            cart_item.amount = amount
        else:
            cart_item.amount += amount

        cart_item.save()

        cart_items_count = CartItem.objects.filter(user=request.user).aggregate(Sum('amount'))
        total_items = cart_items_count['amount__sum'] if cart_items_count['amount__sum'] is not None else 0
        return JsonResponse({'authenticated': True, 'total_items': total_items})

class RemoveFromCartView(View):
    @method_decorator(login_required(login_url=reverse_lazy('app:login')))
    def post(self, request):
        itemID = (request.POST.get('itemID'))
        
        if (itemID is None):
            CartItem.objects.filter(user=request.user).delete()
        else:
            CartItem.objects.filter(user=request.user, commodities__c_id=itemID).delete()

        return HttpResponse('')
    
class UpdateCartView(View):
    @method_decorator(login_required(login_url=reverse_lazy('app:login')))
    def post(self, request):
        cart_items = request.POST.get('cart_items')
        cart_items = (json.loads(cart_items))
        for item in cart_items:
            item_id = item['itemId']
            quantity = item['quantity']

            # filter the CartItem queryset with specific commodities_id and user
            cart_item = CartItem.objects.filter(commodities__c_id=item_id, user=request.user)
            # update the amount field
            cart_item.update(amount=quantity)

        return HttpResponse('')
    
class CheckoutCartView(View):
    @method_decorator(login_required(login_url=reverse_lazy('app:login')))
    def post(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        if (len(cart_items) < 1):
            return JsonResponse({'error': 'No item to checkout'}, status=404)
        
        for cart_item in cart_items:
            purchase = Purchase()
            purchase.user = cart_item.user
            purchase.commodities = cart_item.commodities
            purchase.amount = cart_item.amount
            purchase.save()
        CartItem.objects.filter(user=request.user).delete()

        return HttpResponse("Thank you for your purchase! Your items have been added to your profile.")
    
class UploadProfileImageView(View):
    @method_decorator(login_required(login_url=reverse_lazy('app:login')))
    def post(self, request):
        if 'picture' in request.FILES:
            user_profile = request.user.userprofile
            user_profile.picture = request.FILES['picture']
            user_profile.save()
            image_url = user_profile.picture.url
            return JsonResponse({'image_url': image_url})

        return HttpResponseBadRequest()

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

# @login_required
# def addShoppingCart(request, c_id):
#     c = Commodities.objects.get(c_id = c_id)
#     shoppingCart, created = ShoppingCart.objects.get_or_create(
#         user=request.user,
#         commodities=c,
#         defaults={'amount': 1}
#     )
#     if not created:
#         shoppingCart.quantity += 1
#         shoppingCart.save()
#     return redirect('')

# @login_required
# def removeShoppingCart(request, c_id):
#     '''
#     shoppingCart = request.session.get('cart', {})
#     ShoppingCart.remove()
#     '''
#     shoppingCart = ShoppingCart(request)
#     commodities = get_object_or_404(Commodities, c_id=c_id)
#     shoppingCart.remove(commodities)
#     return redirect('cart')