from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponse
from math import ceil
from datetime import datetime
import json,uuid
from .models import Product, Contact, Order
from .forms import contactForm, userRegistration
from .mail_helper import *


def index(request):
    searchVal = request.GET.get('s')
    allProds = []
    prods = []
    catprods = Product.objects.values('category', 'id')

    cats = {item['category'] for item in catprods}
    for cat in cats:
        if searchVal:
            prod = Product.objects.filter(category=cat).filter(
                Q(product_name__icontains = searchVal) |
                Q(desc__icontains = searchVal) |
                Q(category__icontains = searchVal)
            )
        else:
            prod = Product.objects.filter(category=cat)
            # prod = [item for item in prod if searchMatch(searchVal, item)]

        if len(prod) != 0:
            prods.append(prod)

    prods.sort(key=len, reverse=True)
    for prod in prods:
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # print(User.username)
    params = {'allProds': allProds, 'pageName': 'home'}
    return render(request, 'shop/index.html', params)


def registration(request):
    if request.method == 'POST':
        form = userRegistration(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/shop')
    else:
        form = userRegistration()
    return render(request, 'registration/register.html', {'form': form})


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
        data.save()
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
    if request.method == 'POST':
        email = request.POST.get('email')
        orderId = request.POST.get('order_id')
        try:
            order = Order.objects.get(order_id=orderId, email=email)
        except Order.DoesNotExist:
            return render(request, 'shop/tracker.html', {'pageName': 'checkout'})
        return render(request, 'shop/tracker.html', {'pageName': 'checkout'})
    else:
        return render(request, 'shop/tracker.html',{'pageName': 'tracker'})


def productView(request, pid):
    #fetching product by id
    product = Product.objects.filter(id=pid)
    return render(request, 'shop/prodView.html', {'product': product[0],'pageName': 'productView'})


@login_required(login_url='../login')
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
        order_details['currentSite'] = request.get_host
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