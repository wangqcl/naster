#客户关系表
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from common.models import Users,Compinfo
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

#首页
def index(request,uid):
    print(uid)
    try:
        user = Users.objects.get(id=uid)
        content = {"user":user}
        return render(request,"myadmin/lation/index.html",content)
    except Exception as err:
        print(err)
        context = {'info': '失败！'}
    return render(request, 'myadmin/info.html', context)

def add(request,uid):
    '''添加'''
    try:
        ob = Users.objects.exclude(state=3).get(id=uid)
        la_list = Compinfo.objects.all()
        context = {
            'user': ob,
            'la_list':la_list
        }
        return render(request, 'myadmin/lation/add.html', context)
    except Exception as err:
        print(err)
        context = {'info': '打开失败！'}
    return render(request, 'myadmin/info.html', context)

def insert(request):
    '''执行添加'''
    # try:
    #     a = Users.objects.get(username=request.POST['username'])  #获取用户
    #     compinfo_id = int(request.POST['comp_name'])
    #     b = Compinfo.objects.get(id=compinfo_id)    #获取业务信息
    #     b.users.add(a)  #执行多对多添加
    #     context = {'info': '保存成功！'}
    # except Exception as err:
    #     print(err)
    #     context = {'info': '保存失败！'}
    # return render(request, 'myadmin/info.html', context)
    user_id = int(request.GET.get('id'))
    comp_id = int(request.GET.get('selected_val'))
    '''输出用户对用的所有业务信息'''
    g2 = Users.objects.get(id=user_id)
    comp_list = g2.compinfo_set.all()   #获取用户下所有的业务信息
    repeat_statu = True
    for obj in comp_list:   #判断是否重复添加
        #print(obj.comp_name)
        if obj.id == comp_id:
            repeat_statu = False
            context = {'msg': 'repeat'}
            return JsonResponse(context)

    if repeat_statu == True:
        try:
            user = Users.objects.get(id=user_id)       #获取用户
            Comp = Compinfo.objects.get(id=comp_id)    #获取业务信息
            Comp.users.add(user)                          #执行多对多添加
            context = {'msg': 'success'}
        except Exception as err:
            print(err)
            context = {'msg': 'fail'}
        return JsonResponse(context)

def delete(request,uid):
    '''删除权限'''
    try:
        user_id = request.GET.get('k')
        user = Users.objects.get(id=user_id)
        Comp = Compinfo.objects.get(id=uid)
        user.compinfo_set.remove(Comp)
        print("删除的用户ID：%s"%uid)
        return redirect(reverse('myadmin_lation_index', kwargs={'uid':user_id}))
    except Exception as err:
        print(err)
        context = {'info': '删除失败！'}
        return render(request, 'myadmin/info.html', context)

def edit(request):
    pass

def update(request):
    pass