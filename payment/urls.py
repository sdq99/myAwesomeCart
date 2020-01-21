from django.conf.urls import url
from . import  views

urlpatterns = [
    url('process', views.payment_process, name='process')
]