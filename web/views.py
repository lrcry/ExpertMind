from django.shortcuts import render_to_response
from django.shortcuts import render

# def index(request):
#     return render_to_response('index.html')


def index(request):
    return render(request, 'index.html', {})


def login(request):
    return render(request, 'login.html', {})