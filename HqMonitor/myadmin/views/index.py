from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import check_password

from common.models import Users,Compinfo
import time,json

# 后台首页
def index(request):
    '''后台首页'''
    us_count = Users.objects.exclude(state=3).all().count()
    co_count = Compinfo.objects.exclude(state=3).all().count()
    context = {
        "us_count":us_count,
        "co_count":co_count
    }
    return render(request,"myadmin/index.html",context)

# ==============后台管理员操作====================
# 会员登录表单
def login(request):
    return render(request,'myadmin/login.html')

# 会员执行登录
def dologin(request):
    # 校验验证码
    verifycode = request.session['verifycode']
    code = request.POST['code'].upper()
    if verifycode != code:
        context = {'info': '验证码错误！'}
        return render(request, "myadmin/login.html", context)
    # 判断是否有特殊字符!@_
    user_name = request.POST['username']
    string = "~#$%^&*()+-*/<>,.[]\/"
    for i in string:
        if i in user_name:
            context = {'info': '您的输入包含特殊字符,请重新输入！'}
            return render(request, "myadmin/login.html", context)

    try:
        user = Users.objects.get(username=user_name)
        passw = request.POST['password']
        if user.state == 0:
            ps_bool = check_password(passw,user.password)
            if ps_bool == True:
                request.session['adminuser'] = user.username
                return redirect(reverse('myadmin_index'))
            else:
                context = {'info': '登录账号/密码错误！'}
        else:
            context = {'info': '无登录权限！'}
    except:
        context = {'info': '登录账号/密码错误！'}
    return render(request, "myadmin/login.html", context)

# 会员退出
def logout(request):
    del request.session['adminuser']
    return redirect(reverse('myadmin_login'))

# 会员登录表单
def verify(request):
    import random
    from PIL import Image, ImageDraw, ImageFont
    bgcolor = (242,164,247)
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
    request.session['verifycode'] = rand_str
    import io
    buf = io.BytesIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')