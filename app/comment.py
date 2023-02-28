from django.shortcuts import render, HttpResponse, redirect
from app import models

def commit(request):
    if request.method == "GET":
        content = request.GET.get('content')
        order_id = request.GET.get('order_id')
        models.Comment.objects.create(order_id=order_id, content=content)
    return render('app/home.html')