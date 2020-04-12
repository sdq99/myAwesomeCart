from django.urls import path, include
from . import views
from .api import router

urlpatterns = [
    path('',views.index),
    path('login',views.login),
    path('accounts/', include('allauth.urls')),

    path('api/v1/', include(router.urls)),
]