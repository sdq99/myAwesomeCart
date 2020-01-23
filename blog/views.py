from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    data_dict = {'name': 'SADIQUE'}
    return render(request, 'blog/index.html', data_dict)
