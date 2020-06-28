# default_app_config = 'web.apps.AppConfig'

from common.models import Users,Compinfo
from django.http import HttpResponse


def check_user_request(func):
    name = func.__name__

    def wrapper(*args,**kwargs):
        req = args[1]
        username = req.session.get('webuser',default=None)  # 获取登录用户名
        user = Users.objects.get(username=username)
        status = int(user.state)
        userid = user.id
        if req.method == 'GET':
            comid = int(req.GET.get('comid',1))
        else:
            comid = int(req.data.get('comid',1))
        if status == 0:
            return func(*args, **kwargs)
        if comid != 0:
            comp = Compinfo.objects.get(id=comid)
            id = comp.users.all()
            list = []
            for i in id:
                list.append(i.id)
            if userid not in list:
                return HttpResponse("request error", status=403)
            else:
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return wrapper

#判断是否有修改权限
def user_edit(func):
    name = func.__name__

    def wrapper(*args,**kwargs):
        req = args[0]
        username = req.session.get('webuser',default=None)  # 获取登录用户名
        user = Users.objects.get(username=username)
        userid = req.POST['user']
        if user.id == int(userid):
            return func(*args, **kwargs)
        else:
            return HttpResponse("request error", status=403)

    return wrapper
