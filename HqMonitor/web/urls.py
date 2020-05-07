from django.conf.urls import url

from web.views import index

urlpatterns = [
    # 前台首页
    url(r'^$', index.index, name="web_index"),
    url(r'^test$', index.test, name="web_test"),
    url(r'^login$', index.login, name="web_login"),

]