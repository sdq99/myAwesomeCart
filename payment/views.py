from django.shortcuts import render, get_object_or_404, reverse
from paypal.standard.forms import PayPalPaymentsForm
from shop.models import Order
from django.conf import settings
from django.utils.html import format_html
from django.forms.models import model_to_dict
import json
from django.core.serializers import serialize


class ExtPayPalPaymentsForm(PayPalPaymentsForm):
    def render(self):
        form_open  = u'''<form action="%s" id="PayPalForm" method="post">''' % (self.get_endpoint())
        form_close = u'</form>'
        # format html as you need
        submit_elm = u'''<button type="submit" value="Buy Now" name="submit" title="PayPal - The safer, easier way to pay online!" class="paypalbutton btn btn-block btn-warning font-weight-light">Pay with <img src="/media/payment/paypal-logo.png"></button>'''
        return format_html(form_open+self.as_p()+submit_elm+form_close)

def payment_detail(request):
    if(request.method == 'POST'):
        ordeId = request.Get.get('orderId')
    else:
        orderId = request.session.get('orderId')
    host = request.get_host()
    order = get_object_or_404(Order, order_id = orderId)
    items = json.loads(order.items)

    orderData = {
            'orderId': order.order_id,
            'items': items,
            'name': order.name,
            'email': order.email,
            'phone': order.phone,
            'address': order.address,
            'state': order.state,
            'zip': order.zip,
            'total_price': order.total_price,
        }
    paypal_dict = {
        'cmd': '_cart',
        'upload': 1,
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'currency_code': 'USD',
        'invoice': order.order_id,
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_url': 'http://{}{}'.format(host, reverse('payment_cancelled')),
    }
    for i, value in enumerate(items.values(), 1):
        paypal_dict['item_name_{}'.format(i)] = value['name']
        paypal_dict['amount_{}'.format(i)] = value['price']
        paypal_dict['quantity_{}'.format(i)] = value['qty']
        paypal_dict['item_number_{}'.format(i)] = 9

    form = ExtPayPalPaymentsForm(initial = paypal_dict)
    return  render(request, 'payment/order-detail.html', {'form': form, 'order': orderData})
