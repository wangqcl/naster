from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

# 后台首页
def index(request):
    '''后台首页'''
    #return HttpResponse("欢迎进入后台首页！")
    return render(request,"myadmin/index.html")