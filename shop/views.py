from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.template import Context
from django.template.loader import render_to_string,get_template
from django.http import HttpResponse
from math import ceil
from datetime import datetime
import json,uuid
from .models import Product, Contact, Order
from .forms import contactForm
from .mail_helper import *

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
    if request.method == 'POST':
        order_details = {}
        order_details['items'] = request.POST.get('items')
        order_details['itemList'] = json.loads(order_details['items'] )
        order_details['name'] = request.POST.get('fname') + " " + request.POST.get('lname')
        order_details['email'] = request.POST.get('email')
        order_details['phone'] = request.POST.get('phone')
        order_details['address'] = request.POST.get('address')
        order_details['state'] = request.POST.get('state')
        order_details['zip'] = request.POST.get('zip')
        order_details['totalPrice'] = sum(item['price'] for item in order_details['itemList'] .values())
        order_details['orderId'] = str(uuid.uuid4()).rsplit('-')[-1]
        order_details['orderDate'] = datetime.now().strftime('%b %-d, %Y')
        order = Order(
            order_id = order_details['orderId'],
            items = order_details['items'],
            name = order_details['name'],
            email = order_details['email'],
            phone = order_details['phone'],
            address = order_details['address'],
            state = order_details['state'],
            zip = order_details['zip'],
            total_price = order_details['totalPrice'],
        )
        order.save()
        request.session['orderId'] = str(order.order_id)

        #send mail
        txty = render_to_string('shop/order_confirm_email.html', order_details)
        htmly = render_to_string('shop/order_confirm_email.html', order_details)
        order_success_mail(
            order_details['name'],
            htmly,
            txty,
            order_details['email'],
        )

        # return  render(request, 'shop/order_confirm_email.html', order_details) #to check mail template
        return redirect('/payment/payment-detail')
    else:
        return render(request, 'shop/checkout.html', {'pageName': 'checkout'})

@csrf_exempt
def payment_done(request):
    return render(request, 'shop/payment_done.html')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'shop/payment_cancelled.html')