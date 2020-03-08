from django.shortcuts import get_object_or_404
from .models import Order
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == 'Completed':
        order = get_object_or_404(Order, order_id = ipn.invoice)

        if order.total_price == ipn.mc_gross:
            order.payment_status = 1
            order.save()
