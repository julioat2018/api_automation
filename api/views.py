# from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from selenium import webdriver


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the api index.")


@require_http_methods(["POST"])
def auto_submit(request):
    name = request.POST.get('name')
    surname = request.POST.get('surname')
    password = request.POST.get('password')
    email = request.POST.get('email')
    site_id = request.POST.get('site_id')

    if site_id == 'energia':
        print("energia")
        pass
    elif site_id == 'telefonia':
        print("telefonia")
        pass

    return HttpResponse("Hello, world. You're at the api auto_submit.")


