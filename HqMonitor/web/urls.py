from django.conf.urls import url
from . import views
from .views import center,monit,threaten,score,Invasion
from .views.monit import * #Main_visit_port,Server_status_code,Domain_infor,Ip_fraction,Request_traffic,Response_traffic,Waf_attack_trend,Attack_map,Access_ip,Main_getnum,Hit,Source_data
from .views.threaten import thattack,thhit,thactive,threat,thnews,indexs
from .views.score import mainthr,totalthr,tithr,webthr,inthr,scindex
from .views.Invasion import *
from .views.safety import *

urlpatterns = [
    # 登录
    url(r'^$', center.login, name="login"),  # 登录页面
    url(r'^dologin$', center.dologin, name="dologin"),  # 登录操作
    url(r'^logout$', center.logout, name="logout"),  # 退出操作
    url(r'^verify$', center.verify, name="verify"),  # 验证码

    url(r'^web/center$', center.center, name="web_center"),  #个人中心

    #管理员网络全局信息监控路由
    url(r'^web/index/(?P<pIndex>[0-9]+)$', monit.index, name="monit_index"), #全局信息监控首页
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

    #威胁情报
    url(r'^web/threaten/indexs$',indexs.as_view(), name="monit_threaten_indexs"), #威胁情报监控首页
    # url(r'^web/threaten/index/(?P<pIndex>[0-9]+)$', threaten.index, name="monit_threaten_index"), #威胁情报监控首页
    url(r'^web/threaten/thattack$',thattack.as_view(),name="monit_threaten_thattack"),  #攻击类型
    url(r'^web/threaten/thhit$',thhit.as_view(),name="monit_threaten_thhit"),  #命中趋势
    url(r'^web/threaten/thactive$',thactive.as_view(),name="monit_threaten_thactive"),  #活跃攻击源
    url(r'^web/threaten/threat$',threat.as_view(),name="monit_threaten_threat"),  #IP威胁分类
    url(r'^web/threaten/thnews$',thnews.as_view(),name="monit_threaten_thnews"),  #IP威胁情报源

    #综合评分
    url(r'^web/score/scindex$', scindex.as_view(), name="monit_score_scindex"),  # 综合评分首页
    # url(r'^web/score/index/(?P<pIndex>[0-9]+)$', score.index, name="monit_score_index"), #综合评分首页
    url(r'^web/score/mainthr$',mainthr.as_view(),name="monit_score_mainthr"),#主要威胁IP分值
    url(r'^web/score/totalthr$',totalthr.as_view(),name="monit_score_totalthr"),#总威胁趋势
    url(r'^web/score/tithr$',tithr.as_view(),name="monit_score_tithr"),#TI威胁趋势
    url(r'^web/score/webthr$',webthr.as_view(),name="monit_score_webthr"),#WEB威胁安全趋势
    url(r'^web/score/inthr$',inthr.as_view(),name="monit_score_inthr"),#WEB威胁安全趋势

    #入侵检测
    url(r'^web/Invasion$', indexs.as_view(), name='monit_invasion_index'),  # 首页
    url(r'^web/allattrack$', All_attrack.as_view(), name='monit_all_attrack'),  # 【入侵检测】总攻击数
    url(r'^web/attrackclass$', Attrack_classification.as_view(), name='monit_attrack_class'),  # 【入侵检测】主要攻击类型攻击方式分类
    url(r'^web/mainattrack$', Main_attrack.as_view(), name='monit_main_attrack'),  # 【入侵检测】主要攻击类型
    url(r'^web/attrackport$', Attrack_port.as_view(), name='monit_attrack_port'),  # 【入侵检测】主要受攻击端口
    url(r'^web/attracktype$', Attrack_type.as_view(), name='monit_attrack_type'),  # 【入侵检测】主要攻击类型占比柱状图

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