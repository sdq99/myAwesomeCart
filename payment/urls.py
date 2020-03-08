from django.conf.urls import url,include
from django.urls import path
from . import views

urlpatterns = [
    # url('paypal-process', views.paypal_process, name='paypal-process'),
    url('payment-detail', views.payment_detail, name='payment-detail'),
    path('paypal', include('paypal.standard.ipn.urls')),
]