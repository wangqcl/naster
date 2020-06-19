from django.shortcuts import render
from django.http import HttpResponse
from common.models import Users, Compinfo
from django.utils.decorators import method_decorator
from elasticsearch import Elasticsearch
import json
import datetime
from django.views.generic import View
from django.conf import settings

'''配置es'''
es = Elasticsearch(
    settings.IP_LOCAL,
    http_auth=settings.H_AUTH,
    scheme="http",
    port=9200,
)


class Safety_index(View):
        def get(self, request):
            comid = request.GET.get('comid',None)
            # comid = request.GET.get('comid', 0)  #企业ID
            result =self.seardat(comid)
            print(comid)
            if request.is_ajax() ==False:
                username = request.session.get('webuser', default=None)  # 获取登录用户名
                user = Users.objects.get(username=username)
                content = {
                    "compid":comid,
                }
                if user.state == 0:
                    if int(comid) == 0:
                        return render(request, "web/safety.html", content)
                    else:
                        return render(request, "web/usermon/qsafety.html", content)
                elif user.state == 1 or comid != 0:
                    comp = Compinfo.objects.get(id=comid)
                    users = comp.users.all()
                    for us in users:
                        if us.username == username:
                            return render(request, "web/usermon/qsafety.html", content)  # 用户的监控首页
                        else:
                            content = {"info": "查询失败！"}
                    return render(request, "web/monweb/info.html", content)
                else:
                    error = "访问出错！"
                    content = {"info": error}
                    return render(request, "web/monweb/info.html", content)

        def seardat(self, comid):
            ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区是按 秒和毫秒为整数
            st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-1)).strftime('%Y-%m-%dT%H:%M:00')
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
                        match_phrase = {"match_phrase": {"dst_ip.ip": ip}}
                        sp_param["bool"]["should"].append(match_phrase)
                    self.es_result = self.sear_info(st_time, ed_time, sp_param)
                    if self.es_result == False:
                        return False
                    else:
                        return self.es_result
                except Exception as err:
                    return False


# 验证用户权限
def comd_user(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('username') and request.GET.get('comid'):
            return HttpResponse('404')
        comp_id = Compinfo.objects.get(id=request.GET.get('comid'))
        user = Users.objects.filter(username=request.session.get('username'))
        if user.id != comp_id:
            return False
        return view_func(request, *args, **kwargs)
        # print("自定义装饰器被调用路径为%s" % request.path)

    return wrapper


# 攻击趋势
# @method_decorator(comd_user, name='dispatch')
class Safety_attack_trend(View):
    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=-15)).strftime('%Y-%m-%dT%H:%M:00')
        comid = request.GET.get('comid', None)
        if comid == None:  # 用户信息
            sp_param = None
            es_result = self.sear_info(st_time, ed_time, sp_param)
            return HttpResponse(es_result)
        else:
            try:
                comp = Compinfo.objects.get(id=comid)
                comp_realm = comp.comp_realm  # 域名
                comp_s = comp_realm.split('.', 1)
                sp_param = "*%s*" % (comp_s[1])
                es_result = self.sear_info(st_time, ed_time, sp_param)
                return HttpResponse(es_result)
            except Exception as err:
                print(err)
                return HttpResponse("Error")
        # es_result = self.sear_info(st_time,ed_time)
        # return HttpResponse(es_result)

    def post(self, request):
        info = {"请求失败！"}
        return HttpResponse(info)

    def sear_info(self, st_time, ed_time, sp_param):
        if sp_param == None:
            body = {
                "aggs": {
                    "2": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "fixed_interval": "30s",
                            "time_zone": "Asia/Shanghai",
                            "min_doc_count": 1
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
                    },
                    {
                        "field": "values._widget_1583487508607.data.uploadTime",
                        "format": "date_time"
                    },
                    {
                        "field": "values._widget_1583990422218.data.uploadTime",
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
                                "exists": {
                                    "field": "transaction.messages.message.keyword"
                                }
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
                        "date_histogram": {
                            "field": "@timestamp",
                            "fixed_interval": "30s",
                            "time_zone": "Asia/Shanghai",
                            "min_doc_count": 1
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
                    },
                    {
                        "field": "values._widget_1583487508607.data.uploadTime",
                        "format": "date_time"
                    },
                    {
                        "field": "values._widget_1583990422218.data.uploadTime",
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
                                "exists": {
                                    "field": "transaction.messages.message.keyword"
                                }
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
            ret = es.search(index='waf*', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            y_date, jsontext, x_data = [], {}, []
            for i in re_data:
                x_data.append(i["key_as_string"][11:-13])  # 获取日期数据并放入列表
                y_date.append(i["doc_count"])  # 获取数据总数
            seen = set()
            result = []
            for item in x_data:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
            jsontext['yAxis'] = y_date  # 数据量
            jsontext['xAxis'] = result  # 日期
            jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


# 攻击分布
class Safety_map(View):
    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=-15)).strftime('%Y-%m-%dT%H:%M:00')
        es_result = self.sear_info(st_time, ed_time)
        # print(st_time)
        return HttpResponse(es_result)

    def post(self, request):
        info = {"请求失败！"}
        return HttpResponse(info)

    def sear_info(self, st_time, ed_time):
        body = {
            "aggs": {
                "filter_agg": {
                    "filter": {
                        "geo_bounding_box": {
                            "ignore_unmapped": "true",
                            "geoip.location": {
                                "top_left": {
                                    "lat": 64.590055,
                                    "lon": -180
                                },
                                "bottom_right": {
                                    "lat": -90,
                                    "lon": 180
                                }
                            }
                        }
                    },
                    "aggs": {
                        "2": {
                            "geohash_grid": {
                                "field": "geoip.location",
                                "precision": 2
                            },
                            "aggs": {
                                "3": {
                                    "geo_centroid": {
                                        "field": "geoip.location"
                                    }
                                }
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
        try:
            ret = es.search(index='logstash-nginx-log', doc_type='_doc', body=body)
            re_data = ret['aggregations']['filter_agg']['2']['buckets']
            # print(re_data)
            jsontext = {}
            geoCoordMap = {'北京': [116.404117, 39.906607]}  # 存放所有坐标 {上海: [121.4648, 31.2891],}
            BJData = []  # [[{name: "尼日利亚",value: 500}, {name: "上海",}]]
            i = 1
            # 遍历返回数据
            for buck in re_data:
                lat_list, bjd_list = [], []
                da_json = {}
                end = {"name": "北京", }
                # doc_count = buck["doc_count"] #数量
                # 经纬度
                lat_list.append(buck["3"]["location"]["lon"])  # 精度
                lat_list.append(buck["3"]["location"]["lat"])  # 纬度
                geoCoordMap[i] = lat_list

                da_json["name"] = i
                da_json["value"] = buck["doc_count"]  # 数量
                bjd_list.append(da_json)
                bjd_list.append(end)
                BJData.append(bjd_list)
                i += 1
            jsontext['edtime'] = ed_time
            jsontext['geoCoordMap'] = geoCoordMap
            jsontext['BJData'] = BJData
            return json.dumps(jsontext, ensure_ascii=False)
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


# WAF攻击趋势
class Safety_waf_attack_trend(View):
    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
        st_time = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d").strftime(
            '%Y-%m-%dT%H:%M:%S')
        es_result = self.sear_info(st_time, ed_time)
        return HttpResponse(es_result)

    def post(self, request):
        info = {"请求失败！"}
        return HttpResponse(info)

    def sear_info(self, st_time, ed_time):
        body = {
            "aggs": {
                "4": {
                    "date_histogram": {
                        "field": "@timestamp",
                        "fixed_interval": "30m",
                        "time_zone": "Asia/Shanghai",
                        "min_doc_count": 1
                    },
                    "aggs": {
                        "5": {
                            "terms": {
                                "field": "transaction.messages.message.keyword",
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
                },
                {
                    "field": "values._widget_1583487508607.data.uploadTime",
                    "format": "date_time"
                },
                {
                    "field": "values._widget_1583990422218.data.uploadTime",
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
        try:
            ret = es.search(index='waf*', doc_type='_doc', body=body)
            re_data = ret['aggregations']['4']['buckets']
            list_date, jsontext, yAxis_data = [], {}, {}

            for i in re_data:
                # 获取当前日期
                date = i["key_as_string"]
                list_date.append(date[11:-10])  # 日期
                ret_buckets = i["5"]["buckets"]

                for v in ret_buckets:
                    port_key = v["key"]  # IP
                    doc_count = v["doc_count"]  # 趋势数量
                    keys = list(yAxis_data.keys())
                    if (port_key in keys):
                        if len(yAxis_data[port_key]) < len(list_date) - 1:
                            diff = len(list_date) - len(yAxis_data[port_key])
                            diff_list = [' ' for _ in range(diff - 1)]
                            yAxis_data[port_key].extend(diff_list)  # 合并补空位
                            yAxis_data[port_key].append(doc_count)
                        else:
                            yAxis_data[port_key].append(doc_count)
                    else:
                        null_list = [' ' for _ in range(len(list_date) - 1)]
                        yAxis_data.setdefault(port_key, null_list).append(doc_count)
                jsontext['yAxis'] = yAxis_data  # 数据量
                jsontext['xAxis'] = list_date  # 日期
                jsontext['port'] = list(yAxis_data.keys())  # 所有域名
                jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


# 攻击TOP10
class Safety_top(View):
    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区时间
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=-15)).strftime('%Y-%m-%dT%H:%M:00')
        # 获取
        comid = request.GET.get('comid', None)
        if comid == None:  # 是否携带用户信息
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
                            "field": "transaction.client_ip.keyword",
                            "order": {
                                "_count": "desc"
                            },
                            "size": 10
                        },
                        "aggs": {
                            "3": {
                                "terms": {
                                    "field": "transaction.client_ip.keyword",
                                    "order": {
                                        "_count": "desc"
                                    },
                                    "size": 10
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
                    },
                    {
                        "field": "values._widget_1583487508607.data.uploadTime",
                        "format": "date_time"
                    },
                    {
                        "field": "values._widget_1583990422218.data.uploadTime",
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
                                "exists": {
                                    "field": "transaction.messages.message.keyword"
                                }
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
                            "field": "transaction.client_ip.keyword",
                            "order": {
                                "_count": "desc"
                            },
                            "size": 10
                        },
                        "aggs": {
                            "3": {
                                "terms": {
                                    "field": "transaction.client_ip.keyword",
                                    "order": {
                                        "_count": "desc"
                                    },
                                    "size": 10
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
                    },
                    {
                        "field": "values._widget_1583487508607.data.uploadTime",
                        "format": "date_time"
                    },
                    {
                        "field": "values._widget_1583990422218.data.uploadTime",
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
                                "exists": {
                                    "field": "transaction.messages.message.keyword"
                                }
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
            ret = es.search(index='waf*', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            ips, number, jsontext = [], [], {}
            for i in re_data:
                ips.append(i['key'])  # 域名ip
                number.append(i['doc_count'])
            jsontext['ips'] = ips
            jsontext['number'] = number
            jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


# 风险占比
class Safety_risk(View):
    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区是按 秒和毫秒为整数
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=-15)).strftime('%Y-%m-%dT%H:%M:00')
        # 获取
        comid = request.GET.get('comid', None)
        if comid == None:  # 是否携带用户信息
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
                    match_phrase = {"match_phrase": {"destination.ip": ip}}
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
                            "field": "transaction.messages.details.severity.keyword",
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
                    },
                    {
                        "field": "values._widget_1583487508607.data.uploadTime",
                        "format": "date_time"
                    },
                    {
                        "field": "values._widget_1583990422218.data.uploadTime",
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
                                "exists": {
                                    "field": "transaction.messages.message.keyword"
                                }
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
                            "field": "transaction.messages.details.severity.keyword",
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
                    },
                    {
                        "field": "values._widget_1583487508607.data.uploadTime",
                        "format": "date_time"
                    },
                    {
                        "field": "values._widget_1583990422218.data.uploadTime",
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
                                "exists": {
                                    "field": "transaction.messages.message.keyword"
                                }
                            },
                            sp_param,
                            {
                                "range": {
                                    "@timestamp": {
                                        "format": "strict_date_optional_time",
                                        "gte": "2020-06-14T16:00:00.000Z",
                                        "lte": "2020-06-15T15:59:59.999Z"
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
            ret = es.search(index='waf*', doc_type='_doc', body=body)
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
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


# 主要受攻击端口占比
class Safety_attack_port(View):
    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区是按 秒和毫秒为整数
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=-15)).strftime('%Y-%m-%dT%H:%M:00')
        # 获取
        comid = request.GET.get('comid', None)
        if comid == None:  # 是否携带用户信息
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
                    match_phrase = {"match_phrase": {"destination.ip": ip}}
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
                            "field": "transaction.host_port",
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
                    },
                    {
                        "field": "values._widget_1583487508607.data.uploadTime",
                        "format": "date_time"
                    },
                    {
                        "field": "values._widget_1583990422218.data.uploadTime",
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
                                "exists": {
                                    "field": "transaction.messages.message.keyword"
                                }
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
                            "field": "transaction.host_port",
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
                    },
                    {
                        "field": "values._widget_1583487508607.data.uploadTime",
                        "format": "date_time"
                    },
                    {
                        "field": "values._widget_1583990422218.data.uploadTime",
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
                                "exists": {
                                    "field": "transaction.messages.message.keyword"
                                }
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
            ret = es.search(index='waf*', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            types, number, jsontext = [], [], {}
            for i in re_data:
                number_dict = {}
                types.append(i['key'])
                number_dict['value'], number_dict['name'] = i['doc_count'], i['key']
                number.append(number_dict)
            jsontext['types'] = types
            jsontext['number'] = number
            jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


# WAF攻击统计
class Safety_waf_attack_count(View):
    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区是按 秒和毫秒为整数
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=-15)).strftime('%Y-%m-%dT%H:%M:00')
        # 获取
        comid = request.GET.get('comid', None)
        if comid == None:  # 是否携带用户信息
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
                    match_phrase = {"match_phrase": {"destination.ip": ip}}
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
                            "field": "@timestamp",
                            "order": {
                                "_count": "desc"
                            },
                            "size": 5
                        },
                        "aggs": {
                            "3": {
                                "terms": {
                                    "field": "transaction.client_ip.keyword",
                                    "order": {
                                        "_count": "desc"
                                    },
                                    "size": 5
                                },
                                "aggs": {
                                    "4": {
                                        "terms": {
                                            "field": "transaction.request.method.keyword",
                                            "order": {
                                                "_count": "desc"
                                            },
                                            "size": 5
                                        },
                                        "aggs": {
                                            "5": {
                                                "terms": {
                                                    "field": "transaction.request.headers.Host.keyword",
                                                    "order": {
                                                        "_count": "desc"
                                                    },
                                                    "missing": "__missing__",
                                                    "size": 5
                                                },
                                                "aggs": {
                                                    "6": {
                                                        "terms": {
                                                            "field": "transaction.request.headers.host.keyword",
                                                            "order": {
                                                                "_count": "desc"
                                                            },
                                                            "missing": "__missing__",
                                                            "size": 5
                                                        },
                                                        "aggs": {
                                                            "7": {
                                                                "terms": {
                                                                    "field": "transaction.request.uri.keyword",
                                                                    "order": {
                                                                        "_count": "desc"
                                                                    },
                                                                    "size": 5
                                                                },
                                                                "aggs": {
                                                                    "8": {
                                                                        "terms": {
                                                                            "field": "transaction.messages.message.keyword",
                                                                            "order": {
                                                                                "_count": "desc"
                                                                            },
                                                                            "size": 5
                                                                        },
                                                                        "aggs": {
                                                                            "9": {
                                                                                "terms": {
                                                                                    "field": "transaction.host_ip.keyword",
                                                                                    "order": {
                                                                                        "_count": "desc"
                                                                                    },
                                                                                    "size": 5
                                                                                }
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
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
                    },
                    {
                        "field": "values._widget_1583487508607.data.uploadTime",
                        "format": "date_time"
                    },
                    {
                        "field": "values._widget_1583990422218.data.uploadTime",
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
                                "exists": {
                                    "field": "transaction.messages.message.keyword"
                                }
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
                        "terms": {
                            "field": "@timestamp",
                            "order": {
                                "_count": "desc"
                            },
                            "size": 5
                        },
                        "aggs": {
                            "3": {
                                "terms": {
                                    "field": "transaction.client_ip.keyword",
                                    "order": {
                                        "_count": "desc"
                                    },
                                    "size": 5
                                },
                                "aggs": {
                                    "4": {
                                        "terms": {
                                            "field": "transaction.request.method.keyword",
                                            "order": {
                                                "_count": "desc"
                                            },
                                            "size": 5
                                        },
                                        "aggs": {
                                            "5": {
                                                "terms": {
                                                    "field": "transaction.request.headers.Host.keyword",
                                                    "order": {
                                                        "_count": "desc"
                                                    },
                                                    "missing": "__missing__",
                                                    "size": 5
                                                },
                                                "aggs": {
                                                    "6": {
                                                        "terms": {
                                                            "field": "transaction.request.headers.host.keyword",
                                                            "order": {
                                                                "_count": "desc"
                                                            },
                                                            "missing": "__missing__",
                                                            "size": 5
                                                        },
                                                        "aggs": {
                                                            "7": {
                                                                "terms": {
                                                                    "field": "transaction.request.uri.keyword",
                                                                    "order": {
                                                                        "_count": "desc"
                                                                    },
                                                                    "size": 5
                                                                },
                                                                "aggs": {
                                                                    "8": {
                                                                        "terms": {
                                                                            "field": "transaction.messages.message.keyword",
                                                                            "order": {
                                                                                "_count": "desc"
                                                                            },
                                                                            "size": 5
                                                                        },
                                                                        "aggs": {
                                                                            "9": {
                                                                                "terms": {
                                                                                    "field": "transaction.host_ip.keyword",
                                                                                    "order": {
                                                                                        "_count": "desc"
                                                                                    },
                                                                                    "size": 5
                                                                                }
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
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
                    },
                    {
                        "field": "values._widget_1583487508607.data.uploadTime",
                        "format": "date_time"
                    },
                    {
                        "field": "values._widget_1583990422218.data.uploadTime",
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
                                "exists": {
                                    "field": "transaction.messages.message.keyword"
                                }
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
            ret = es.search(index='waf*', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            datelist, jsontext = [], {}
            for i in re_data:
                data, data1 = [], []
                data.append(i["key_as_string"][11:-8])
                for j in i['3']['buckets']:
                    data.append(j['key'])
                    for k in j['4']['buckets']:
                        data.append(k['key'])
                        for l in k['5']['buckets']:
                            data.append(l['key'])
                data1.append(data[0])
                if len(data) > 5:
                    datelist.append(data[:4])
                    datelist.append(data1 + data[4:8] if len(data[4:8])>2 else '')
                    datelist.append(data1 + data[7:10] if len(data[7:10])>2 else '')
                    datelist.append(data1 + data[10:13] if len(data[10:13])>2 else '')
                    datelist.append(data1 + data[13:] if len(data[13:])>2 else '')
                # data.pop() and data.pop(-1) and data.pop(-2) if len(data) > 4 else data
                # datelist.append(data)
            jsontext['data'] = datelist[:13]
            jsontext['edtime'] = ed_time
            return json.dumps(jsontext, ensure_ascii=False)
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)