from django.shortcuts import render
from django.http import HttpResponse
from math import ceil

from .models import Product

# Create your views here.
def index(response):
    # products = Product.objects.all()
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))
    allProds = []
    catprods = Product.objects.values('category', 'id')
    print(catprods)
    return 0

def about(response):
    return render(response, 'shop/about.html')

def contact(response):
    return HttpResponse("This is contact page.")

def tracker(response):
    return HttpResponse("hello world.")

def search(response):
    return HttpResponse("hello world.")

def productView(response):
    return HttpResponse("This is product view page.")

def checkout(response):
    return HttpResponse("This is checkout page.")
