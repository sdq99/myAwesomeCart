from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from shop.models import Order
from django.forms.models import model_to_dict
import json
from django.core.serializers import serialize

# Create your views here.
def payment_process(request):
    orderId = request.session.get('orderId')
    print(orderId)
    order = get_object_or_404(Order, order_id = orderId)
    items = json.loads(order.items)

    paypal_dict = {
        'cmd': '_cart',
        'upload': 1,
        'business': 'x786922@gmail.com',
        # 'amount': 22,
        # 'item_name': 'abc,nn',
        'currency_code': 'USD',
        'notify_url': 'http://google.com',
        'return_url': 'http://google.com',
        'cancel_url': 'http://google.com',
    }
    print(items)
    for i, value in enumerate(items.values(), 1):
        paypal_dict['item_name_{}'.format(i)] = value['name']
        paypal_dict['amount_{}'.format(i)] = value['price'][1:]
        paypal_dict['quantity_{}'.format(i)] = value['qty']
        paypal_dict['item_number_{}'.format(i)] = 9

    form = PayPalPaymentsForm(initial = paypal_dict)
    return  render(request, 'payment/process.html', {'form': form})
    # print(request.session['orderId'])
