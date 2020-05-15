from django.shortcuts import render
from django.http import HttpResponse
from common.models import Users,Compinfo
from datetime import datetime
from django.db.models import Q
from django.core.paginator import Paginator

def index(request,pIndex=1):
    '''首页信息展示'''
    umod = Compinfo.objects.all().exclude(state=3).order_by("id") #不包含状态为3的
    mywhere = []
    # 获取判断并封装关键字搜索
    kw = request.GET.get("keyword", None)
    if kw:
        # 查询用户信息
        list = umod.filter(Q(comp_name__contains=kw))
        mywhere.append("keyword=" + kw)
    else:
        list = umod.filter()
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list, 10)  # 分页对象
    maxpages = page.num_pages  # 最大页数
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 当前页数据
    plist = page.page_range  # 页码数列表

    # 封装信息加载模板输出
    context = {"pany_list": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request,"myadmin/pany/index.html",context)

def delete(request,uid):
    '''删除'''
    try:
        ob = Compinfo.objects.get(id=uid)
        # ob.state = 3  #删除用户
        ob.users.remove() #删除所有索引
        ob.delete()
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
        ob.state = request.POST['state']
        ob.comp_ip = request.POST['compip']
        ob.comp_realm = request.POST['comprealm']
        ob.port = request.POST['compport']
        ob.access_status = request.POST['accessstatus']
        ob.access_node = request.POST['accessnode']
        ob.service_items = request.POST['serviceitems']
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
        ob.comp_ip = request.POST['compip']
        ob.comp_realm = request.POST['comprealm']
        ob.state = 1
        ob.port = request.POST['compport']
        ob.access_status = request.POST['accessstatus']
        ob.access_node = request.POST['accessnode']
        ob.service_items = request.POST['serviceitems']
        ob.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': '保存成功！'}
    except Exception as err:
        print(err)
        context = {'info': '保存失败！'}
    return render(request, 'myadmin/info.html', context)

