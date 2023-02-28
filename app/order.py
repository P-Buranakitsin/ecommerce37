from django.shortcuts import render, HttpResponse, redirect
from app import models

def pay(request):
    if request.method == "GET":
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        address = request.GET.get('address')
        message = request.GET.get('message')
        product_name = request.GET.get('product_name')
        num = request.GET.get('num')
        price = request.GET.get('price')
        order = models.Order.objects.create(product_name=product_name, num=num, price=price,
                                   address=address, phone=phone,
                                   name=name, message=message)
        value = {'id': order.id}
        return render(request, 'app/comment.html', value)