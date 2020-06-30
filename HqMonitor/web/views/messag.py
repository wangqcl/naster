from django.shortcuts import render
from django.http import HttpResponse
from common.models import Users,Compinfo,Feedback
from django.views.generic import View
from datetime import datetime
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.db.models import Q

#信息反馈页面
def index(request,pIndex=0):
    us = request.session.get('webuser',default=None)
    user = Users.objects.get(username=us)
    feedlist = Feedback.objects.filter(userid=user.id) #反馈信息

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(feedlist, 5)  # 分页对象
    maxpages = page.num_pages
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)
    plist = page.page_range

    context = {
        "user":user,
        "feedlist":list2,
        'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages
    }
    return render(request, "web/monweb/message.html",context)
#提交反馈
def insert(request):
    us = request.session.get('webuser', default=None)
    user = Users.objects.get(username=us)
    try:
        fe = Feedback()
        fe.userid = user.id
        fe.user_account = user.username
        fe.username = request.POST['name']
        fe.content = request.POST['content']
        fe.feedtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fe.save()
    except Exception as err:
        print(err)
    return redirect(reverse('web_center_messag',kwargs={'pIndex':1}))


#反馈信息查询
class mesquery(View):
    def get(self, request):
        pIndex = request.GET.get('pIndex', 1)
        us = request.session.get('webuser', default=None)
        user = Users.objects.get(username=us)

        if user.state == 0:
            mywhere = []
            feedlist = Feedback.objects.all()  # 反馈信息
            # 获取判断并封装关键字搜索
            kw = request.GET.get("keyword", None)
            if kw:
                # 查询用户信息
                list = feedlist.filter(Q(username__contains=kw) | Q(user_account__contains=kw))
                mywhere.append("keyword=" + kw)
            else:
                list = feedlist.filter()
            #获取内容关键字
            cont = request.GET.get('cont', '')
            if cont != '':
                list = list.filter(Q(content__contains=cont))

        # 执行分页处理
            pIndex = int(pIndex)
            page = Paginator(list, 10)  # 分页对象
            maxpages = page.num_pages
            # 判断页数是否越界
            if pIndex > maxpages:
                pIndex = maxpages
            if pIndex < 1:
                pIndex = 1
            list2 = page.page(pIndex)
            plist = page.page_range

            context = {
                "user": user,
                "feedlist": list2,
                'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages
            }
            return render(request,"web/monweb/messquery.html",context)
        else:
            return HttpResponse("request error", status=403)
    def post(self,request):
        return HttpResponse("request error", status=403)

#回复信息
class messret(View):
    def get(self, request):
        us = request.session.get('webuser', default=None)
        user = Users.objects.get(username=us)
        if user.state == 0:
            feeid = request.GET.get("feed")
            context = {"feeid":feeid}
            return render(request,"web/monweb/messret.html",context)
        else:
            pass
    def post(self,request):
        us = request.session.get('webuser', default=None)
        user = Users.objects.get(username=us)
        if user.state == 0:
            feeid = request.POST["fee"]
            fe = Feedback.objects.get(id=feeid)
            fe.reply_content = request.POST["content"]
            fe.save()
            return redirect(reverse('web_center_mesquery'))

        else:
            return HttpResponse("request error", status=403)


