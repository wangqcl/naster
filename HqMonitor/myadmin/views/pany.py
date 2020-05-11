from django.shortcuts import render
from django.http import HttpResponse
from common.models import Users,Compinfo
from datetime import datetime
from django.core.paginator import Paginator

def index(request):
    '''首页信息展示'''
    pany_list = Compinfo.objects.all().exclude(state=3)
    context = {"pany_list":pany_list}
    return render(request,"myadmin/pany/index.html",context)

def delete(request,uid):
    '''删除'''
    try:
        ob = Compinfo.objects.get(id=uid)
        ob.state = 3  #删除用户
        ob.save()
        context = {'info': '删除成功！'}
    except Exception as err:
        print(err)
        context = {'info': '删除失败！'}
    return render(request, 'myadmin/info.html', context)

def edit(request,uid=None):
    '''编辑'''
    try:
        ob = Compinfo.objects.get(id=uid)
        context = {'comp': ob}
        print(request.session.get('adminuser'))
        return render(request, 'myadmin/pany/edit.html', context)
    except Exception as err:
        print(err)
        context = {'info': '打开失败！'}
    return render(request, 'myadmin/info.html', context)

def update(request,uid):
    '''执行编辑'''
    try:
        ob = Compinfo.objects.get(id=uid)
        # 使用request.POST获取前台的数据
        ob.address = request.POST['address']
        ob.name = request.POST['name']
        #ob.address = request.POST['address']
        ob.state = request.POST['state']
        ob.phone = request.POST['phone']
        ob.comp_ip = request.POST['compip']
        ob.comp_realm = request.POST['comprealm']
        ob.save()
        context = {'info':'保存成功！'}
    except Exception as err:
        print(err)
        context = {'info': '保存失败！'}
    return render(request,'myadmin/info.html',context)

def add(request):
    '''添加'''
    return render(request, "myadmin/pany/add.html")

def insert(request):
    '''执行添加'''
    try:
        ob = Compinfo()
        # 使用request.POST获取前台的数据
        ob.comp_name = request.POST['compname']
        ob.address = request.POST['address']
        ob.name = request.POST['name']
        ob.phone = request.POST['phone']
        ob.comp_ip = request.POST['compip']
        ob.comp_realm = request.POST['comprealm']
        ob.state = request.POST['state']
        ob.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '保存成功！'}
    except Exception as err:
        print(err)
        context = {'info': '保存失败！'}
    return render(request, 'myadmin/info.html', context)

