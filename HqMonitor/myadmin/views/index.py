from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

# Create your views here.
def index(request):
    '''后台首页'''
    return HttpResponse("欢迎进入后台首页！")