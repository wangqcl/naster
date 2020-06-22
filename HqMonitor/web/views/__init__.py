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
        comid = int(req.GET.get('comid'))
        if status == 0:
            return func(*args, **kwargs)
        if comid != 0:
            comp = Compinfo.objects.get(id=comid)
            id = comp.users.all()
            list = []
            for i in id:
                list.append(i.id)
            if userid not in list:
                return HttpResponse("403:您无权访问该数据，请更换id")
            else:
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return wrapper