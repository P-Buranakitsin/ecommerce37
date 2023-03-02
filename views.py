from django.shortcuts import render
from .forms import OrderForm

def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Process the order
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            product_name = form.cleaned_data['product_name']
            quantity = form.cleaned_data['quantity']
            # Calculate total price
            price_per_unit = 10.00 # Example price
            total_price = price_per_unit * quantity
            # Save the order
            # ...
            # Redirect the user to a success page
            return render(request, 'order_success.html')
    else:
        form = OrderForm()
    return render(request, 'order.html', {'form': form})

