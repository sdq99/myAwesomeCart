from django.shortcuts import render, redirect, reverse
from django.template import Context
from django.template.loader import render_to_string,get_template
from django.http import HttpResponse
from math import ceil
from datetime import datetime
import json
from .models import Product, Contact, Order
from .forms import contactForm
from .mail_helper import *


# Create your views here.

def loginSignup(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'shop/loginSignup.html', {'pageName': 'loginSignup'})

def index(request):
    myDate = datetime.now()
    allProds = []
    prods = []
    catprods = Product.objects.values('category', 'id')

    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        prods.append(prod)

    prods.sort(key=len, reverse=True)
    for prod in prods:
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds, 'pageName': 'home'}
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html',{'pageName': 'about'})

def contact(request):
    if request.method == 'POST' :
        postData = {}
        postData['name'] = request.POST.get('name','')
        postData['email'] = request.POST.get('email','')
        postData['phone'] = request.POST.get('phone', '')
        postData['message'] = request.POST.get('message', '')
        print(postData)
        txty = render_to_string('shop/contact_email.txt', postData)
        htmly = render_to_string('shop/contact_email.html', postData)
        data = Contact(name = postData['name'], email = postData['email'], phone = postData['phone'], message = postData['message'])
        data.save();
        response_mail = user_query_mail(
                postData['name'],
                htmly,
                txty,
                postData['email']
            )
        print(response_mail)
        return HttpResponse(json.dumps(response_mail), content_type="application/json")
    else:
        form = contactForm()
        return render(request, 'shop/contact.html', {'form' : form, 'pageName': 'contact'})

def tracker(request):
    # if request.method == 'POST':
    #     pass
    # else:
        return render(request, 'shop/tracker.html',{'pageName': 'tracker'})

def search(request):
    return render(request, 'shop/search.html', {'pageName': 'search'})

def productView(request, pid):
    #fetching product by id
    product = Product.objects.filter(id=pid)
    return render(request, 'shop/prodView.html', {'product': product[0],'pageName': 'productView'})

def checkout(request):
    print(request.method)
    if request.method == 'POST':
        items = request.POST.get('items')
        name = request.POST.get('fname') + " " + request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        state = request.POST.get('state')
        zip = request.POST.get('zip')

        order = Order(items = items, name = name, email = email, phone = phone, address = address, state = state, zip = zip)
        order.save()
        request.session['orderId'] = order.order_id
        # return render(request, 'shop/order_success.html', {'orderId': orderId})
        # return redirect(reverse('payment:process'))
        return redirect('/payment/process')
    else:
        return render(request, 'shop/checkout.html', {'pageName': 'checkout'})
