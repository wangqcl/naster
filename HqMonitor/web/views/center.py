from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from common.models import Users, Compinfo
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import check_password
from . import user_edit, Encryption
import datetime
import base64
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from django.db.models import Q

# Create your views here.


def search(request):
    '''跳转检索的用户个人中心'''

    log_user = request.session['webuser']  # 获取当前登录账号
    userinfo = Users.objects.get(username=log_user)
    name = str(request.GET.get('text'))
    if userinfo.state == 0:  # 判断是否超级管理员
        comp_list = Compinfo.objects.filter(comp_name=name)
    else:
        comp_lists = userinfo.compinfo_set.all()
        comp_list = comp_lists.filter(Q(comp_name=name))
    content = {
        'userinfo': userinfo,
        'comp_list': comp_list
    }
    return render(request, "web/monweb/Center.html", content)




def center(request):
    '''跳转用户个人中心'''
    log_user = request.session['webuser']  # 获取当前登录账号
    userinfo = Users.objects.get(username=log_user)
    if userinfo.state == 0:  # 判断是否超级管理员
        comp_list = Compinfo.objects.exclude(state=2).all()
    else:
        comp_list = userinfo.compinfo_set.all()

    content = {
        'userinfo': userinfo,
        'comp_list': comp_list
    }
    return render(request, "web/monweb/Center.html", content)


def monit_center(request):
    '''登录直接跳转'''
    log_user = request.session['webuser']  # 获取当前登录账号
    userinfo = Users.objects.get(username=log_user)
    if userinfo.state == 0:  # 判断是否超级管理员
        content = {
            'compid':0
        }
        return render(request, "web/monit.html",content)
    else:
        comp_list = userinfo.compinfo_set.all()
        comid = comp_list[0].id
        content = {
            'userinfo': userinfo,
            'comp_list': comp_list,
            'compid':comid
        }
        return render(request, "web/usermon/qmonit.html", content)



# 执行编辑
@user_edit
def edit(request):
    try:
        userid = request.POST['user']
        us = Users.objects.get(id=userid)
        us.name = request.POST['uname']
        us.phone = request.POST['uphone']
        us.email = request.POST['uemail']
        us.save()
        context = {'msg': 'success'}
    except Exception as err:
        print(err)
        context = {'msg': 'fail'}
    return JsonResponse(context)


# ==============后台管理员操作====================
# 会员登录表单
def login(request):
    Encryption(request)
    return render(request, 'web/monweb/login.html')


# 会员执行登录
def dologin(request):
    # 校验验证码
    verifycode = request.session['weblogcode']
    code = request.POST['code']
    code = code.upper()
    if verifycode != code:
        context = {'info': '验证码错误！', 'msg': 'fail'}
        return JsonResponse(context)
    # 判断是否有特殊字符
    user_name = request.POST['username']
    string = "~#$%^&*()+-*/<>,.[]\/"  # 去除特殊字符的正则
    for i in string:
        if i in user_name:
            context = {'info': '您的输入包含特殊字符,请重新输入！', 'msg': 'fail'}
            return JsonResponse(context)
    try:
        # 根据账号获取登录者信息
        user = Users.objects.get(username=user_name)
        passw = request.POST['password']
        passw = passw.encode('utf8')
        RANDOM_GENERATOR = Random.new().read
        with open('web/encryption/master-private.pem') as f:
            key = f.read()
        rsakey = RSA.importKey(key.encode('utf8'))
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        password = cipher.decrypt(base64.b64decode(passw), RANDOM_GENERATOR)
        # 判断是否禁用
        if user.state != 2:
            if int((datetime.datetime.now() - user.login_time).total_seconds()) < 300:
                context = {'info': '账号锁定5分钟内不能登陆!', 'msg': 'fail'}
                return JsonResponse(context)
            if user.count > 4:
                user.login_time = datetime.datetime.now()
                user.count = 0
                user.save()
                context = {'info': '密码输入超过5次，用户锁定5分钟', 'msg': 'fail'}
                return JsonResponse(context)
            ps_bool = check_password(password, user.password)
            if ps_bool == True:
                request.session['webuser'] = user.username
                user.count = 0
                user.save()
                context = {'info': '登陆成功', 'msg': 'success', 'url': '/web/center/monit'}
                return JsonResponse(context)
            user.count += 1
            user.save()
            context = {'info': '登录账号/密码错误！', 'msg': 'fail'}
            return JsonResponse(context)
        else:
            context = {'info': '无登录权限！', 'msg': 'fail'}
            return JsonResponse(context)
    except:
        context = {'info': '用户名不存在！', 'msg': 'fail'}
        return JsonResponse(context)


# 会员退出
def logout(request):
    del request.session['webuser']
    return redirect(reverse('login'))


# 会员登录表单
def verify(request):
    # 引入随机函数模块
    import random
    from PIL import Image, ImageDraw, ImageFont
    bgcolor = (242, 164, 247)
    width = 100
    height = 25
    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    font = ImageFont.truetype('static/consola.ttf', 21)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    del draw
    request.session['weblogcode'] = rand_str
    import io
    buf = io.BytesIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')
