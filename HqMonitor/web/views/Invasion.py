from django.shortcuts import render
from django.http import HttpResponse
from common.models import Users, Compinfo
from elasticsearch import Elasticsearch
import json
import datetime
from django.views.generic import View
from django.conf import settings
from pytz import timezone
import datetime
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage
from . import check_user_request


'''配置es'''
es = Elasticsearch(
    settings.IP_LOCAL,
    http_auth=settings.H_AUTH,
    scheme="http",
    port=9200,
)


# 首页
class indexs(View):

    '''首页-入侵检测信息'''
    @check_user_request
    def get(self, request):
        comid = request.GET.get('comid','None')
        if comid == 'None':
            comid = None
        else:
            comid = int(comid)
        # comid = request.GET.get('comid', 0)  #企业ID
        result =self.seardat(comid)
        res = result["dat"]
        # res = result.get('dat','')
        paginator = Paginator(res, 4)    #分页功能，一页8条数据
        if request.is_ajax() ==False:
            username = request.session.get('webuser', default=None)  # 获取登录用户名
            user = Users.objects.get(username=username)
            userlist = paginator.page(1)
            content = {
                "compid":comid,
                "users":userlist
            }
            if user.state == 0:
                if int(comid) == 0:
                    return render(request, "web/Invasion.html", content)
                else:
                    return render(request, "web/usermon/qinvasion.html", content)
            elif user.state == 1 & comid != 0:
                comp = Compinfo.objects.get(id=comid)
                users = comp.users.all()
                for us in users:
                    if us.username == username:
                        return render(request, "web/usermon/qinvasion.html", content)  # 用户的监控首页
                    else:
                        content = {"info": "查询失败！"}
                return render(request, "web/monweb/info.html", content)
            else:
                error = "访问出错！"
                content = {"info": error}
                return render(request, "web/monweb/info.html", content)

        # Ajax数据交互
        if request.is_ajax():
            page = request.GET.get('page')
            try:
                users = paginator.page(page)
            # 如果页数不是整数，返回第一页
            except PageNotAnInteger:
                users = paginator.page(1)
            # 如果页数不存在/不合法，返回最后一页
            except InvalidPage:
                users = paginator.page(paginator.num_pages)
            user_li = list(users)  #.object_list.values()
            # 分别为是否有上一页false/true，是否有下一页false/true，总共多少页，当前页面的数据
            result = {'has_previous': users.has_previous(),
                      'has_next': users.has_next(),
                      'num_pages': users.paginator.num_pages,
                      'user_li': user_li}
            return JsonResponse(result)

    def seardat(self,comid):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区时间
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-30)).strftime('%Y-%m-%dT%H:%M:00')
        if int(comid) == 0:  # 是否携带用户信息
            sp_param = None
            es_result = self.sear_info(st_time, ed_time, sp_param)
            return es_result
        else:
            try:
                comp = Compinfo.objects.get(id=comid)
                comp_ip = comp.comp_ip  # IP
                comp_s = comp_ip.split(';')
                sp_param = {
                    "bool": {
                        "should": [
                        ],
                        "minimum_should_match": 1
                    }
                }
                for ip in comp_s:
                    match_phrase = {"match_phrase": {"dst_ip": ip}}
                    sp_param["bool"]["should"].append(match_phrase)
                self.es_result = self.sear_info(st_time, ed_time, sp_param)
                if self.es_result == False:
                    return False
                else:
                    return self.es_result
            except Exception as err:
                # logger.error('请求出错：{}'.format(err))
                print(err)
                return False

    def sear_info(self, st_time, ed_time,sp_param):
        if sp_param == None:
            body = {
            "version": "true",
            "size": 30,
            "sort": [
                {
                    "@timestamp": {
                        "order": "desc",
                        "unmapped_type": "boolean"
                    }
                }
            ],
            "_source": {
                "excludes": []
            },
            "stored_fields": [
                "*"
            ],
            "script_fields": {},
            "docvalue_fields": [
                {
                    "field": "@timestamp",
                    "format": "date_time"
                }
            ],
            "query": {
                "bool": {
                    "must": [],
                    "filter": [
                        {
                            "match_all": {}
                        },
                        {
                            "match_all": {}
                        },
                        {
                            "range": {
                                "@timestamp": {
                                    "format": "strict_date_optional_time",
                                    "gte": st_time,
                                    "lte": ed_time
                                }
                            }
                        }
                    ],
                    "should": [],
                    "must_not": []
                }
            },
            "highlight": {
                "pre_tags": [
                    "@kibana-highlighted-field@"
                ],
                "post_tags": [
                    "@/kibana-highlighted-field@"
                ],
                "fields": {
                    "*": {}
                },
                "fragment_size": 2147483647
            }
        }
        else:
            body = {
                "version": "true",
                "size": 30,
                "sort": [
                    {
                        "@timestamp": {
                            "order": "desc",
                            "unmapped_type": "boolean"
                        }
                    }
                ],
                "_source": {
                    "excludes": []
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {},
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    }
                ],
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "match_all": {}
                            },
                            sp_param,
                            {
                                "range": {
                                    "@timestamp": {
                                        "format": "strict_date_optional_time",
                                        "gte": st_time,
                                        "lte": ed_time
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": []
                    }
                },
                "highlight": {
                    "pre_tags": [
                        "@kibana-highlighted-field@"
                    ],
                    "post_tags": [
                        "@/kibana-highlighted-field@"
                    ],
                    "fields": {
                        "*": {}
                    },
                    "fragment_size": 2147483647
                }
            }
        try:
            ret = es.search(index='snort', doc_type='_doc', body=body)
            re_data = ret['hits']['hits']
            datalist,jstext = [],{}
            for v in re_data:
                jsontext = {}
                da_list = v.get('_source','')
                jsontext['time']=da_list.get('@timestamp','')  # 时间
                jsontext['ip']=da_list.get('src_ip','') # ip
                jsontext['port']=da_list.get('dst_port','')  #端口
                jsontext['title']=da_list.get('title','')   #标题
                jsontext['url']=da_list.get('urls','')   #URL
                datalist.append(jsontext)
            jstext['dat'] = datalist
            return jstext
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


# 【入侵检测】总攻击数

class All_attrack(View):


    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区是按 秒和毫秒为整数
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-30)).strftime('%Y-%m-%dT%H:%M:00')
        # 获取
        comid = request.GET.get('comid','None')
        if comid == 'None':
            comid = None
        else:
            comid = int(comid)
        if type(comid) != int:  # 是否携带用户信息
            sp_param = None
            es_result = self.in_all(st_time, ed_time, sp_param)
            return HttpResponse(es_result)
        else:
            try:
                comp = Compinfo.objects.get(id=comid)
                comp_ip = comp.comp_ip  # IP
                comp_s = comp_ip.split(';')
                sp_param = {
                    "bool": {
                        "should": [
                        ],
                        "minimum_should_match": 1
                    }
                }
                for ip in comp_s:
                    match_phrase = {"match_phrase": {"dst_ip": ip}}
                    sp_param["bool"]["should"].append(match_phrase)
                es_result = self.in_all(st_time, ed_time, sp_param)
                return HttpResponse(es_result)
            except Exception as err:
                print(err)
                return HttpResponse("Error")


    def post(self, request):
        info = {"请求失败！"}
        return HttpResponse(info)


    def in_all(self, st_time, ed_time,sp_param):
        if sp_param == None:
            body = {
                "aggs": {},
                "size": 0,
                "_source": {
                    "excludes": []
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {},
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    }
                ],
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "match_all": {}
                            },
                            {
                                "range": {
                                    "@timestamp": {
                                        "format": "strict_date_optional_time",
                                        "gte": st_time,
                                        "lte": ed_time
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": []
                    }
                }
            }
        else:
            body = {
                "aggs": {},
                "size": 0,
                "_source": {
                    "excludes": []
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {},
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    }
                ],
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "match_all": {}
                            },
                            sp_param,
                            {
                                "range": {
                                    "@timestamp": {
                                        "format": "strict_date_optional_time",
                                        "gte": st_time,
                                        "lte": ed_time
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": []
                    }
                }
            }
        try:
            invasion_all = {}
            list = []
            ret = es.search(index='snort', doc_type='_doc', body=body)
            re_data = ret['hits']['total']['value']
            list.append(str(re_data))
            invasion_all['key'] = list
            return json.dumps(invasion_all)
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


# 【入侵检测】主要攻击类型攻击方式分类
class Attrack_classification(View):

    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区是按 秒和毫秒为整数
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-30)).strftime('%Y-%m-%dT%H:%M:00')
        # 获取
        comid = request.GET.get('comid')
        if comid:
            comid = int(comid)
        else:
            comid = None
        if type(comid) != int:  # 是否携带用户信息
            sp_param = None
            es_result = self.sear_info(st_time, ed_time, sp_param)
            return HttpResponse(es_result)
        else:
            try:
                comp = Compinfo.objects.get(id=comid)
                comp_ip = comp.comp_ip  # IP
                comp_s = comp_ip.split(';')
                sp_param = {
                    "bool": {
                        "should": [
                        ],
                        "minimum_should_match": 1
                    }
                }
                for ip in comp_s:
                    match_phrase = {"match_phrase": {"dst_ip": ip}}
                    sp_param["bool"]["should"].append(match_phrase)
                es_result = self.sear_info(st_time, ed_time, sp_param)
                return HttpResponse(es_result)
            except Exception as err:
                print(err)
                return HttpResponse("Error")

    def post(self, request):
        info = {"请求失败！"}
        return HttpResponse(info)

    def sear_info(self, st_time, ed_time, sp_param):
        if sp_param == None:
            body ={
                "aggs": {
                    "2": {
                        "terms": {
                            "field": "Classification.keyword",
                            "order": {
                                "_count": "desc"
                            },
                            "size": 5
                        },
                        "aggs": {
                            "3": {
                                "terms": {
                                    "field": "title.keyword",
                                    "order": {
                                        "_count": "desc"
                                    },
                                    "size": 5
                                }
                            }
                        }
                    }
                },
                "size": 0,
                "_source": {
                    "excludes": []
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {},
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    }
                ],
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "match_all": {}
                            },
                            {
                                "range": {
                                    "@timestamp": {
                                        "format": "strict_date_optional_time",
                                        "gte": st_time,
                                        "lte": ed_time
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": []
                    }
                }
            } # 全部
        else:
            body ={
                "aggs": {
                    "2": {
                        "terms": {
                            "field": "Classification.keyword",
                            "order": {
                                "_count": "desc"
                            },
                            "size": 5
                        },
                        "aggs": {
                            "3": {
                                "terms": {
                                    "field": "title.keyword",
                                    "order": {
                                        "_count": "desc"
                                    },
                                    "size": 5
                                }
                            }
                        }
                    }
                },
                "size": 0,
                "_source": {
                    "excludes": []
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {},
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    }
                ],
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "match_all": {}
                            },
                            sp_param,
                            {
                                "range": {
                                    "@timestamp": {
                                        "format": "strict_date_optional_time",
                                        "gte": st_time,
                                        "lte": ed_time
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": []
                    }
                }
            }  # 按域名筛选

        try:
            ret = es.search(index='snort', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            type, method, show,all = [], [], [],{}
            color = ['#5045f6', '#ff4343', '#ffed25', '#45dbf7', '#0089fa', '#ba58ff', '#fe9336', '#3eff74', '#06f0ab', '#7b7c68', '#e5b5b5', '#f0b489', '#928ea8']
            for index,i in enumerate(re_data):
                lab1 = {}
                show.append(i.get('key',''))
                lab1['value'] = i.get('doc_count','')
                lab1['name'] = i.get('key','')
                lab1['itemStyle'] = {
                    "normal": {
                        "color": color[index]
                    }
                }
                type.append(lab1)
                for indexs,j in enumerate(i.get('3','').get('buckets','')):
                    lab2 = {}
                    lab2['value'] = j.get('doc_count','')
                    lab2['name'] = j.get('key','')
                    lab2['itemStyle'] = {
                        "normal": {
                            "color": color[indexs]
                        }
                    }
                    show.append(j.get('key',''))
                    method.append(lab2)
            all['type']=type
            all['method']=method
            all['show']=show
            return json.dumps(all)
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


# 【入侵检测】主要攻击类型
class Main_attrack(View):
    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-30)).strftime('%Y-%m-%dT%H:%M:00')
        # 获取
        comid = request.GET.get('comid')
        if comid:
            comid = int(comid)
        else:
            comid = None
        if type(comid) != int:  # 是否携带用户信息
            sp_param = None
            es_result = self.sear_info(st_time, ed_time, sp_param)
            return HttpResponse(es_result)
        else:
            try:
                comp = Compinfo.objects.get(id=comid)
                comp_ip = comp.comp_ip  # IP
                comp_s = comp_ip.split(';')
                sp_param = {
                    "bool":
                        {
                            "should":
                                [

                                ],
                            "minimum_should_match": 1
                        }
                }
                for ip in comp_s:
                    match_phrase = {"match_phrase": {"dst_ip": ip}}
                    sp_param["bool"]["should"].append(match_phrase)
                es_result = self.sear_info(st_time, ed_time, sp_param)
                return HttpResponse(es_result)
            except Exception as err:
                print(err)
                return HttpResponse("Error")
        # es_result = self.sear_info(st_time, ed_time)
        # return HttpResponse(es_result)

    def post(self, request):
        info = {"请求失败！"}
        return HttpResponse(info)

    def sear_info(self, st_time, ed_time,sp_param):
        if sp_param == None:
            body = {
                "aggs": {
                    "2": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "fixed_interval": "48h",
                            "time_zone": "Asia/Shanghai",
                            "order": {
                                "_count": "desc"
                            }
                        },
                        "aggs": {
                            "3": {
                                "terms": {
                                    "field": "Classification.keyword",
                                    "order": {
                                        "_count": "desc"
                                    },
                                    "size": 5
                                }
                            }
                        }
                    }
                },
                "size": 0,
                "_source": {
                    "excludes": []
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {},
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    }
                ],
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "match_all": {}
                            },
                            {
                                "range": {
                                    "@timestamp": {
                                        "format": "strict_date_optional_time",
                                        "gte": st_time,
                                        "lte": ed_time
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": []
                    }
                }
            }
        else:
            body = {
                "aggs": {
                    "2": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "fixed_interval": "48h",
                            "time_zone": "Asia/Shanghai",
                            "order": {
                                "_count": "desc"
                            }
                        },
                        "aggs": {
                            "3": {
                                "terms": {
                                    "field": "Classification.keyword",
                                    "order": {
                                        "_count": "desc"
                                    },
                                    "size": 5
                                }
                            }
                        }
                    }
                },
                "size": 0,
                "_source": {
                    "excludes": []
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {},
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    }
                ],
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "match_all": {}
                            },
                            sp_param,
                            {
                                "range": {
                                    "@timestamp": {
                                        "format": "strict_date_optional_time",
                                        "gte": st_time,
                                        "lte": ed_time
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": []
                    }
                }
            }
        try:
            ret = es.search(index='snort', doc_type='_doc', body=body)
            re_data = ret.get('aggregations','').get('2','').get('buckets','')
            name, linex, line, jsontext = [],[], [] ,{}
            color = ['#00b9f6', '#38a97d', '#004eff', '#17c7e7', '#4e85ea', '#e49be9', '#078d9d', '#eca52a', '#ef9544', '#ea3b3b']
            for i in re_data:
                string = self.time(i.get('key_as_string'))
                linex.append(string)
                key = i.get('3','').get('buckets','')
                for j in key:
                    if j.get('key','') not in name:
                        name.append(j.get('key',''))
            for index,n in enumerate(name):
                value = []
                series = {}
                for i in re_data:
                    key = i.get('3','').get('buckets','')
                    values = [stu for stu in key if n in stu["key"]]
                    if values != []:
                        value.append(values[0].get('doc_count',''))
                    else:
                        value.append(0)
                series['name'] = n
                series['type'] = 'line'
                series['yAxisIndex'] = 0
                series['symbolSize'] = 12
                series['itemStyle'] ={
                    "normal":{
                    "color": color[index],
                }}
                series['data'] = value
                line.append(series)
            jsontext['name'] = name
            jsontext['linex'] = linex
            jsontext['value'] = line
            return json.dumps(jsontext)
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)

    def time(self,utc_time):
        n_time = datetime.datetime.strptime(utc_time,'%Y-%m-%dT%H:%M:%S.%f+08:00')
        utctime = datetime.datetime(n_time.year,n_time.month,n_time.day,n_time.hour,n_time.minute,n_time.second,tzinfo=timezone('UTC'))
        lt = utctime.astimezone(timezone('Asia/Shanghai'))
        llt = lt.strftime("%Y%m%d")
        return llt



# 【入侵检测】主要受攻击端口
class Attrack_port(View):

    def get(self,request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区是按 秒和毫秒为整数
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-30)).strftime('%Y-%m-%dT%H:%M:00')
        #获取
        comid = request.GET.get('comid')
        if comid:
            comid = int(comid)
        else:
            comid = None
        if type(comid) != int:  # 是否携带用户信息
            sp_param = None
            es_result = self.sear_info(st_time, ed_time, sp_param)
            return HttpResponse(es_result)
        else:
            try:
                comp = Compinfo.objects.get(id=comid)
                comp_ip = comp.comp_ip  # IP
                comp_s = comp_ip.split(';')
                sp_param ={
                    "bool": {
                        "should": [
                        ],
                        "minimum_should_match": 1
                    }
                }
                for ip in comp_s:
                    match_phrase = {"match_phrase": {"dst_ip": ip}}
                    sp_param["bool"]["should"].append(match_phrase)
                es_result = self.sear_info(st_time, ed_time, sp_param)
                return HttpResponse(es_result)
            except Exception as err:
                print(err)
                return HttpResponse("Error")
    def post(self,request):
        info = {"请求失败！"}
        return HttpResponse(info)

    def sear_info(self,st_time,ed_time,sp_param):
        if sp_param == None:
            body = {
                "aggs": {
                    "2": {
                        "terms": {
                            "field": "dst_port.keyword",
                            "order": {
                                "_count": "desc"
                            },
                            "size": 10
                        }
                    }
                },
                "size": 0,
                "_source": {
                    "excludes": []
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {},
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    }
                ],
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "match_all": {}
                            },
                            {
                                "range": {
                                    "@timestamp": {
                                        "format": "strict_date_optional_time",
                                        "gte": st_time,
                                        "lte": ed_time
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": []
                    }
                }
            } #全部
        else:
            body = {
                "aggs": {
                    "2": {
                        "terms": {
                            "field": "dst_port.keyword",
                            "order": {
                                "_count": "desc"
                            },
                            "size": 10
                        }
                    }
                },
                "size": 0,
                "_source": {
                    "excludes": []
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {},
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    }
                ],
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "match_all": {}
                            },
                            sp_param,
                            {
                                "range": {
                                    "@timestamp": {
                                        "format": "strict_date_optional_time",
                                        "gte": st_time,
                                        "lte": ed_time
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": []
                    }
                }
            } #按域名筛选
        try:
            ret = es.search(index='snort', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            ports, number, jsontext = [], [], {}
            for i in re_data:
                number_dict = {}
                ports.append(i['key'])
                number_dict['value'], number_dict['name'] = i['doc_count'], i['key']
                number.append(number_dict)
            jsontext['ports'] = ports
            jsontext['number'] = number
            jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except:
            errinfo = {"error":"数据请求失败！"}
            return HttpResponse(errinfo)


# 【入侵检测】主要攻击类型占比
class Attrack_type(View):
    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区时间
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-30)).strftime('%Y-%m-%dT%H:%M:00')
        # 获取
        comid = request.GET.get('comid')
        if comid:
            comid = int(comid)
        else:
            comid = None
        if type(comid) != int:  # 是否携带用户信息
            sp_param = None
            es_result = self.sear_info(st_time, ed_time, sp_param)
            return HttpResponse(es_result)
        else:
            try:
                comp = Compinfo.objects.get(id=comid)
                comp_ip = comp.comp_ip  # IP
                comp_s = comp_ip.split(';')
                sp_param = {
                    "bool":
                        {
                            "should":
                                [

                                ],
                            "minimum_should_match": 1
                        }
                }
                for ip in comp_s:
                    match_phrase = {"match_phrase": {"dst_ip": ip}}
                    sp_param["bool"]["should"].append(match_phrase)
                es_result = self.sear_info(st_time, ed_time, sp_param)
                return HttpResponse(es_result)
            except Exception as err:
                print(err)
                return HttpResponse("Error")

    def post(self, request):
        info = {"请求失败！"}
        return HttpResponse(info)

    def sear_info(self, st_time, ed_time, sp_param):
        if sp_param == None:
            body = {
                "aggs": {
                    "2": {
                        "terms": {
                            "field": "Classification.keyword",
                            "order": {
                                "_count": "desc"
                            },
                            "size": 5
                        }
                    }
                },
                "size": 0,
                "_source": {
                    "excludes": []
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {},
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    }
                ],
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "match_all": {}
                            },
                            {
                                "range": {
                                    "@timestamp": {
                                        "format": "strict_date_optional_time",
                                        "gte": st_time,
                                        "lte": ed_time
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": []
                    }
                }
            }  # 全部
        else:
            body = {
                "aggs": {
                    "2": {
                        "terms": {
                            "field": "Classification.keyword",
                            "order": {
                                "_count": "desc"
                            },
                            "size": 5
                        }
                    }
                },
                "size": 0,
                "_source": {
                    "excludes": []
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {},
                "docvalue_fields": [
                    {
                        "field": "@timestamp",
                        "format": "date_time"
                    }
                ],
                "query": {
                    "bool": {
                        "must": [],
                        "filter": [
                            {
                                "match_all": {}
                            },
                            {
                                "match_all": {}
                            },
                            sp_param,
                            {
                                "range": {
                                    "@timestamp": {
                                        "format": "strict_date_optional_time",
                                        "gte": st_time,
                                        "lte": ed_time
                                    }
                                }
                            }
                        ],
                        "should": [],
                        "must_not": []
                    }
                }
            } # 按域名筛选
        try:
            ret = es.search(index='snort', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            type, number, jsontext = [], [], {}
            for i in re_data:
                type.append(i['key'])  # 域名
                ip_frac = i['doc_count']
                number.append(round(ip_frac))  # 分值,四舍五入
            jsontext['types'] = type
            jsontext['number'] = number
            jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)




