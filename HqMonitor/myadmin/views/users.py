from django.shortcuts import render
from django.http import HttpResponse
from common.models import Users,Compinfo
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password

from random import Random
from hashlib import md5

# 浏览会员
def index(request,pIndex=1):
    umod = Users.objects.exclude(state=3).order_by("id")
    mywhere = []

    #获取判断并封装关键字搜索
    kw = request.GET.get("keyword",None)
    if kw:
        #查询用户信息
        list = umod.filter(Q(username__contains=kw) | Q(name__contains=kw))
        mywhere.append("keyword=" + kw)
    else:
        list = umod.filter()
    # 获取、判断并封装性别sex搜索条件
    sex = request.GET.get('sex', '')
    if sex != '':
        list = list.filter(sex=sex)
        mywhere.append("sex=" + sex)

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
    context = {"userslist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, "myadmin/users/index.html", context)

# 会员信息添加表单
def add(request):
    return render(request, "myadmin/users/add.html")

#执行会员信息添加
def insert(request):
    try:
        ob = Users()
        ob.username = request.POST['username']
        ob.name = request.POST['name']
        passw = request.POST['password']
        dj_ps = make_password(passw, None, 'pbkdf2_sha256') #加密
        ob.password = dj_ps
        ob.phone = request.POST['phone']
        ob.email = request.POST['email']
        ob.state = 1
        ob.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':'保存成功！'}
    except Exception as err:
        print(err)
        context = {'info': '保存失败！'}
    return render(request,'myadmin/info.html',context)

# 执行会员信息删除
def delete(request,uid):
    try:
        ob = Users.objects.get(id=uid)
        ob.compinfo_set.remove()
        ob.delete()
        context = {'info': '删除成功！'}
    except Exception as err:
        print(err)
        context = {'info': '删除失败！'}
    return render(request, 'myadmin/info.html', context)

# 打开会员信息编辑表单
def edit(request,uid):
    try:
        ob = Users.objects.get(id=uid)
        context = {'user': ob}
        return render(request, 'myadmin/users/edit.html', context)
    except Exception as err:
        print(err)
        context = {'info': '打开失败！'}
    return render(request, 'myadmin/info.html', context)

# 执行会员信息编辑
def update(request,uid):
    try:
        ob = Users.objects.get(id=uid)
        ob.name = request.POST['name']
        ob.phone = request.POST['phone']
        ob.email = request.POST['email']
        ob.state = request.POST['state']
        ob.save()
        context = {'info':'保存成功！'}
    except Exception as err:
        print(err)
        context = {'info': '保存失败！'}
    return render(request,'myadmin/info.html',context)

#密码修改页面
def resetpass(request,uid):
    try:
        ob = Users.objects.get(id=uid)
        context = {'user': ob}
        return render(request, 'myadmin/users/resetpass.html', context)
    except Exception as err:
        print(err)
        context = {'info': '打开失败！'}
    return render(request,'myadmin/info.html',context)

#执行密码修改

def doresetpass(request,uid):
    try:
        ob = Users.objects.get(id=uid)
        passw = request.POST['password']
        dj_ps = make_password(passw, None, 'pbkdf2_sha256')
        ob.password = dj_ps
        ob.save()
        context = {"info": "密码重置成功！"}
    except Exception as err:
        print(err)
        context = {"info": "密码重置失败"}
    return render(request, "myadmin/info.html", context)