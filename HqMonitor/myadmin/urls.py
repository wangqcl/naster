from django.conf.urls import url

from myadmin.views import index,users,pany

urlpatterns = [
    # 后台首页
    url(r'^$', index.index, name="myadmin_index"),
    # 后台用户管理
    #url(r'^users/$', users.index, name="myadmin_users_index"),  # 会员首页
    url(r'^users/(?P<pIndex>[0-9]+)$', users.index, name="myadmin_users_index"),   #会员首页
    url(r'^users/add$', users.add, name="myadmin_users_add"),  # 添加会员
    url(r'^users/insert$', users.insert, name="myadmin_users_insert"),  # 执行添加
    url(r'^users/del/(?P<uid>[0-9]+)$', users.delete, name="myadmin_users_del"),  # 删除会员
    url(r'^users/edit/(?P<uid>[0-9]+)$', users.edit, name="myadmin_users_edit"),  # 编辑会员
    url(r'^users/update/(?P<uid>[0-9]+)$', users.update, name="myadmin_users_update"),  # 更新会员
    url(r'^users/resetpass/(?P<uid>[0-9]+)$', users.resetpass, name="myadmin_users_resetpass"),  # 修改密码
    url(r'^users/doresetpass/(?P<uid>[0-9]+)$', users.doresetpass, name="myadmin_users_doresetpass"),  # 执行密码修改

    # 后台管理员路由
    url(r'^login$', index.login, name="myadmin_login"),  # 登录页面
    url(r'^dologin$', index.dologin, name="myadmin_dologin"),  # 登录操作
    url(r'^logout$', index.logout, name="myadmin_logout"),  # 退出操作
    url(r'^verify$', index.verify, name="myadmin_verify"),  # 验证码

    #公司信息维护
    url(r'^pany$', pany.index, name="myadmin_pany_index"),   #会员首页
    url(r'^pany/add$', pany.add, name="myadmin_pany_add"),  # 添加会员
    url(r'^pany/insert$', pany.insert, name="myadmin_pany_insert"),  # 执行添加
    url(r'^pany/del/(?P<uid>[0-9]+)$', pany.delete, name="myadmin_pany_del"),  # 删除会员
    url(r'^pany/edit/(?P<uid>[0-9]+)$', pany.edit, name="myadmin_pany_edit"),  # 编辑会员
    url(r'^pany/update/(?P<uid>[0-9]+)$', pany.update, name="myadmin_pany_update"),  # 更新会员

]
