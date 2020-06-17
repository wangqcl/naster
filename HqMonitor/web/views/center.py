from django.shortcuts import render
from django.http import HttpResponse
from common.models import Users,Compinfo
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import check_password

# Create your views here.

def center(request):
    '''跳转用户个人中心'''
    log_user = request.session['webuser'] #获取当前登录账号
    userinfo = Users.objects.get(username=log_user)
    if userinfo.state == 0:#判断是否超级管理员
        comp_list = Compinfo.objects.exclude(state=2).all()
    else:
        comp_list = userinfo.compinfo_set.all()

    content = {
        'userinfo':userinfo,
        'comp_list':comp_list
    }
    return render(request, "web/monweb/Center.html",content)

# ==============后台管理员操作====================
# 会员登录表单
def login(request):
    return render(request,'web/monweb/login.html')

# 会员执行登录
def dologin(request):
    # 校验验证码
    verifycode = request.session['weblogcode']
    code = request.POST['code']
    code = code.upper()
    if verifycode != code:
        context = {'info': '验证码错误！'}
        return render(request, "web/monweb/login.html", context)
    # 判断是否有特殊字符
    user_name = request.POST['username']
    print(user_name)
    string = "~#$%^&*()+-*/<>,.[]\/"  #去除特殊字符的正则
    for i in string:
        if i in user_name:
            print(i)
            context = {'info': '您的输入包含特殊字符,请重新输入！'}
            return render(request, "web/monweb/login.html", context)

    try:
        # 根据账号获取登录者信息
        user = Users.objects.get(username=user_name)
        passw = request.POST['password']
        # 判断是否禁用
        if user.state != 2:
            ps_bool = check_password(passw, user.password)
            if ps_bool == True:
                request.session['webuser'] = user.username
                return redirect(reverse('web_center'))
            else:
                context = {'info': '登录账号/密码错误！'}
        else:
            context = {'info': '无登录权限！'}
    except:
        context = {'info': '登录账号/密码错误！'}
    return render(request, "web/monweb/login.html", context)

# 会员退出
def logout(request):
    del request.session['webuser']
    return redirect(reverse('login'))

# 会员登录表单
def verify(request):
    #引入随机函数模块
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
    request.session['weblogcode'] = rand_str
    import io
    buf = io.BytesIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')