from django.db import models
from datetime import datetime

#用户信息模型
class Users(models.Model):
    username = models.CharField(max_length=32) #账号
    name = models.CharField(max_length=16,null=True)      #真实姓名
    password = models.CharField(max_length=128)  #密码
    phone = models.CharField(max_length=16,null=True)     #电话
    email = models.CharField(max_length=50,null=True)     #Emai
    state = models.IntegerField(default=1)      #状态
    login_time = models.DateTimeField(default=datetime.now)      #登录锁定时间
    count = models.IntegerField(default=0)      #登录错误次数
    addtime = models.DateTimeField(default=datetime.now)    #注册时间

    # def toDict(self):
    #     return {'id':self.id,'username':self.username,'name':self.name,'password':self.password,'phone':self.phone,'email':self.email,'state':self.state,'comp_id':self.comp_id,'addtime':self.addtime}
    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"  # 更改表名

#公司信息表
class Compinfo(models.Model):
    comp_name = models.CharField(max_length=16)  # 企业名称
    comp_ip = models.CharField(max_length=32)  # 企业IP
    comp_realm = models.CharField(max_length=32)  # 企业域名
    state = models.IntegerField(default=1) #企业信息状态
    addtime = models.DateTimeField(default=datetime.now)  # 维护时间
    port = models.IntegerField(null=True) #端口
    access_status = models.IntegerField(default=1)   #接入状态
    access_node = models.CharField(max_length=32,default="")   #接入节点
    service_items = models.CharField(max_length=32,default="") #服务
    users = models.ManyToManyField(to='Users')  #多对多关系对应
    leak_scan = models.CharField(max_length=32,null=True) #服务项

    def toDict(self):
        return {'id':self.id,'comp_name':self.comp_name,'comp_ip':self.comp_ip,'comp_realm':self.comp_realm,'state':self.state,'addtime':self.addtime,'port':self.port,'access_status':self.access_status,'access_node':self.access_node,'service_items':self.service_items,'Leak_scan':self.leak_scan}

    class Meta:
        db_table = "compinfo"  # 更改表名


class Feedback(models.Model):
    userid = models.IntegerField() #用户ID
    username = models.CharField(max_length=16,null=True)
    content = models.TextField(null=True)
    feedtime = models.DateTimeField(default=datetime.now)
    reply_content = models.CharField(max_length=255)
    user_account = models.CharField(max_length=32)  # 账号

    def toDict(self):
        return {'userid':self.userid,'username':self.username,'content':self.content,'feedtime':self.feedtime,'reply_content':self.reply_content}

    class Meta:
        ordering = ['-feedtime'] #排序
        db_table = "feedback"  # 更改表名