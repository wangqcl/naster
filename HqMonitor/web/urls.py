from django.conf.urls import url
from . import views
from .views import center,monit,safety
from .views.monit import Main_visit_port,Server_status_code,Domain_infor,Ip_fraction,Request_traffic,Response_traffic,Waf_attack_trend,Attack_map,Access_ip,Main_getnum,Hit,Source_data
from .views.safety import Safety_attack_trend,Safety_index,Safety_map,Safety_top,Safety_attack_port,Safety_risk,Safety_waf_attack_count,Safety_waf_attack_trend

urlpatterns = [
    #管理员网络全局信息监控路由
    url(r'^web/index/(?P<pIndex>[0-9]+)$', monit.index, name="monit_index"), #首页
    url(r'^web/getnum$', Main_getnum.as_view(), name="monit_main_getnum"),#请求数量折线图
    url(r'^web/visitport$', Main_visit_port.as_view(), name='monit_visitport'), # 主要访问端口
    url(r'^web/statuscode$', Server_status_code.as_view(), name='monit_status_code'), # 服务器状态码
    url(r'^web/domain$', Domain_infor.as_view(), name='monit_domain_infor'), # 域名被访问次数/时间
    url(r'^web/fraction$', Ip_fraction.as_view(), name='monit_ip_fraction'), # IP分值
    url(r'^web/rqtraffic$', Request_traffic.as_view(), name='monit_Request_traffic'),  # 客户端请求流量
    url(r'^web/rstraffic$', Response_traffic.as_view(), name='monit_Response_traffic'),  # 客户端响应流量
    url(r'^web/trend$', Waf_attack_trend.as_view(), name='monit_attack_trend'),  # waf攻击趋势
    url(r'^web/attackmap$', Attack_map.as_view(), name='monit_attack_map'),  # 地图趋势
    url(r'^web/accessip$', Access_ip.as_view(), name='monit_Access_ip'),  # 地图趋势
    url(r'^web/Hit$', Hit.as_view(), name='monit_Hit'),  # 命中
    url(r'^web/Source_data$', Source_data.as_view(), name='monit_Source_data'),  # 流量数据

    url(r'^web/center$', center.center, name="web_center"),  #个人中心

    #登录
    url(r'^$', center.login, name="login"),  # 登录页面
    url(r'^dologin$', center.dologin, name="dologin"),  # 登录操作
    url(r'^logout$', center.logout, name="logout"),  # 退出操作
    url(r'^verify$', center.verify, name="verify"),  # 验证码


    #web安全防护信息
    url(r'^web/safety$', Safety_index.as_view(), name="safety_index"),   # 安全主页
    url(r'^web/attacktrend$', Safety_attack_trend.as_view(), name='safety_attack_trend'), # 攻击趋势
    url(r'^web/safetymap$', Safety_map.as_view(), name='safety_map'), # 攻击分布
    url(r'^web/wafattack$', Safety_waf_attack_trend.as_view(), name='safety_waf_attack_trend'), # WAF攻击趋势
    url(r'^web/safetytop$', Safety_top.as_view(), name='safety_top'), # 攻击TOP10
    url(r'^web/safety_risk$', Safety_risk.as_view(), name='safety_risk'), # 风险占比
    url(r'^web/attackport$', Safety_attack_port.as_view(), name='safety_attack_port'), # 主要受攻击端口占比
    url(r'^web/wafattackcount$', Safety_waf_attack_count.as_view(), name='safety_waf_attack_count'), # WAF攻击统计

]