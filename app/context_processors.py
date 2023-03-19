from .models import CartItem
from django.db.models import Sum

def cart_item_count(request):
    if request.user.is_authenticated:
        # Count the number of items in the user's cart
        cart_items_count = CartItem.objects.filter(user=request.user).aggregate(Sum('amount'))
        total_items = cart_items_count['amount__sum'] if cart_items_count['amount__sum'] is not None else 0
        count = total_items
    else:
        # If the user is not authenticated, set the count to zero
        count = 0
    # Return the count as a dictionary
    return {'cart_item_count': count}