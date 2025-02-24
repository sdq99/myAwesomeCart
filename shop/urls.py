from django.urls import path, include
# from django.conf.urls import include
from . import  views

urlpatterns = [
    path("", views.index, name = "ShopHome"),

    # auth
    path('', include('django.contrib.auth.urls') ),
    path('register/', views.registration, name= 'register'),

    path("about/", views.about, name = "AboutUs"),
    path("contact/", views.contact, name = "ContactUs"),
    path("tracker/", views.tracker, name = "TrackingStatus"),
    path("products/<int:pid>", views.productView, name = "ProductView"),
    path("checkout/", views.checkout, name = "Checkout"),
    # path('paypal', include('paypal.standard.ipn.urls')),
    path('payment', include('payment.urls'), name= "payment"),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
]

