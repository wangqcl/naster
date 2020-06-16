from django.shortcuts import render
from django.http import HttpResponse
from common.models import Users,Compinfo

#威胁情报监控页面
def index(request,pIndex=0):

    username = request.session.get('webuser', default=None)  # 获取登录用户名
    user = Users.objects.get(username=username)

    if user.state == 0:
        if int(pIndex) == 0:
            content = {
                "compid": pIndex
            }
            return render(request, "web/threaten.html", content)
        else:
            content = {
                "compid": pIndex
            }
            return render(request, "web/usermon/qthreaten.html", content)  # 只查询此用户下的数据
    elif user.state == 1 & pIndex != 0:
        comp = Compinfo.objects.get(id=pIndex)
        users = comp.users.all()  # 所有的用户账号
        for us in users:
            if us.username == username:
                content = {
                    "compid": pIndex
                }
                return render(request, "web/usermon/threaten.html", content)  # 用户的监控首页
            else:
                content = {"info": "查询失败！"}
        return render(request, "web/info.html", content)
    else:
        error = "访问出错！"
        content = {"info": error}
        return render(request, "web/info.html", content)