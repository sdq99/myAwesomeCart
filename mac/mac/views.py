from django.http import HttpResponse

def index(response):
    return HttpResponse("<a href='shop'>shop</a> <a href='blog'>blog</a>")