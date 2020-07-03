from django.shortcuts import render
from django.http import HttpResponse
from common.models import Users,Compinfo
from elasticsearch import Elasticsearch
import json
import datetime
from django.views.generic import View
from django.conf import settings
from . import check_user_request

import logging
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage

logger = logging.getLogger('log')
'''配置es'''
es = Elasticsearch(
    settings.IP_LOCAL,
    http_auth=settings.H_AUTH,
    scheme="http",
    timeout=30,
    port=9200,
)


# 首页
class Safety_index(View):
    '''首页-web安全信息'''

    @check_user_request
    def get(self, request):
        username = request.session.get('webuser', default=None)  # 获取登录用户名
        user = Users.objects.get(username=username)
        pIndex = request.GET.get('comid', None)
        content = {
            "compid": pIndex,
        }
        if user.state == 0:
            if int(pIndex) == 0:
                return render(request, "web/safety.html", content)
            else:
                return render(request, "web/usermon/qsafety.html", content)
        elif user.state == 1:
            return render(request, "web/usermon/qsafety.html", content)  # 用户的监控首页

    def seardat(self, comid):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区时间
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
                    match_phrase = {"match_phrase": {"transaction.host_ip.keyword": ip}}
                    sp_param["bool"]["should"].append(match_phrase)
                self.es_result = self.sear_info(st_time, ed_time, sp_param)
                return HttpResponse(self.es_result)
            except Exception as err:
                print(err)
                return HttpResponse("Error")

    def seardate(self, comid, time):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区时间
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-time)).strftime('%Y-%m-%dT%H:%M:00')
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
                    match_phrase = {"match_phrase": {"transaction.host_ip.keyword": ip}}
                    sp_param["bool"]["should"].append(match_phrase)
                self.es_result = self.sear_info(st_time, ed_time, sp_param)
                return HttpResponse(self.es_result)
            except Exception as err:
                print(err)
                return HttpResponse("Error")

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
            jsonlist, jsontext = [], {}
            for i in re_data:  # 多个
                buck_a = i['3']['buckets']
                for v in buck_a:  # 多个
                    try:
                        jsontext_1 = {}
                        # 遍历数据
                        buck_b = v['4']['buckets']
                        y_id = v['key']  # 源IP
                        y_count = v['doc_count']  # 数量
                        jsontext_1["y_id"] = y_id
                        jsontext_1["y_count"] = y_count
                        for k in buck_b:
                            jsontext_1["w_type"] = k['key']  # 威胁情报类型
                            buck_c = k['5']['buckets']
                            for c in buck_c:
                                waf_ym = c['key']  # 域名
                                jsontext_1["waf_ym"] = waf_ym
                                buck_d = c['6']['buckets']
                                for d in buck_d:
                                    buck_d = d['7']['buckets']
                                    for l in buck_d:
                                        waf_lj = l['key']
                                        jsontext_1["waf_lj"] = waf_lj  # waf拦截器
                        jsonlist.append(jsontext_1)
                    except Exception as err:
                        continue
            jsontext['dat'] = jsonlist
            return jsontext
        except Exception as err:
            logger.error('威胁统计-数据-获取数据出错：{}'.format(err))
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


# 攻击趋势
class Safety_attack_trend(View):

    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=-1)).strftime('%Y-%m-%dT%H:%M:00')
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
                            "should": [],
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
        time = request.POST['tim']
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
        if time == 'None':
            st_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=-1)).strftime('%Y-%m-%dT%H:%M:00')
        else:
            st_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=-int(time))).strftime('%Y-%m-%dT%H:%M:00')
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
                            "should": [],
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
                x_data.append(i["key_as_string"].replace("T", " ")[11:-13])  # 获取日期数据并放入列表
                y_date.append(i["doc_count"])  # 获取数据总数
            jsontext['yAxis'] = y_date[1::2]  # 数据量
            jsontext['xAxis'] = x_data[1::2]  # 日期
            jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except Exception as err:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


# 攻击分布
class Safety_map(View):

    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-1)).strftime('%Y-%m-%dT%H:%M:00')
        comid = request.GET.get('comid', None)
        if comid == None:  # 全局信息
            param = None
            sp_param = None
            es_result = self.sear_info(st_time, ed_time, sp_param, param)
            return HttpResponse(es_result)
        else:
            try:
                comp = Compinfo.objects.get(id=comid)
                comp_realm = comp.comp_realm
                if comp_realm == "":  # 域名为空
                    param = 1
                    comp_ip = comp.comp_ip  # IP
                    comp_s = comp_ip.split(';')
                    sp_param = {
                        "bool":
                            {
                                "should":
                                    [],
                                "minimum_should_match": 1
                            }
                    }
                    for ip in comp_s:
                        match_phrase = {"match_phrase": {"domain": ip}}
                        sp_param["bool"]["should"].append(match_phrase)
                    es_result = self.sear_info(st_time, ed_time, sp_param, param)
                    return HttpResponse(es_result)
                else:
                    param = 2
                    comp_s = comp_realm.split('.', 1)
                    sp_param = "*%s*" % (comp_s[1])
                    es_result = self.sear_info(st_time, ed_time, sp_param, param)
                    return HttpResponse(es_result)
            except Exception as err:
                print(err)
                return HttpResponse("Error")

    def post(self, request):
        tim = request.POST['tim']
        comid = request.POST['compid']
        if tim == "None":
            ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
            st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-1)).strftime('%Y-%m-%dT%H:%M:00')
        else:
            ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
            st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-int(tim))).strftime('%Y-%m-%dT%H:%M:00')

        if int(comid) == 0:  # 是否携带用户信息
            param = None
            sp_param = None
            es_result = self.sear_info(st_time, ed_time, sp_param, param)
            return HttpResponse(es_result)
        else:
            try:
                comp = Compinfo.objects.get(id=comid)
                comp_realm = comp.comp_realm
                if comp_realm == "":  # 域名为空
                    param = 1
                    comp_ip = comp.comp_ip  # IP
                    comp_s = comp_ip.split(';')
                    sp_param = {
                        "bool":
                            {
                                "should":
                                    [],
                                "minimum_should_match": 1
                            }
                    }
                    for ip in comp_s:
                        match_phrase = {"match_phrase": {"domain": ip}}
                        sp_param["bool"]["should"].append(match_phrase)
                    es_result = self.sear_info(st_time, ed_time, sp_param, param)
                    return HttpResponse(es_result)
                else:
                    param = 2
                    comp_s = comp_realm.split('.', 1)
                    sp_param = "*%s*" % (comp_s[1])
                    es_result = self.sear_info(st_time, ed_time, sp_param, param)
                    return HttpResponse(es_result)
            except Exception as err:
                print(err)
                return HttpResponse("Error")

    def sear_info(self, st_time, ed_time, sp_param, param):
        if sp_param == None:
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
        elif param == 1:  # IP
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
        elif param == 2:  # 域名
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
                                "bool": {
                                    "should": [
                                        {
                                            "wildcard": {
                                                "domain": sp_param
                                            }
                                        }
                                    ],
                                    "minimum_should_match": 1
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
            return HttpResponse(json.dumps(jsontext))
        except Exception as err:
            print(err)
            return HttpResponse("Error")


# WAF攻击趋势
class Safety_waf_attack_trend(View):

    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
        st_time = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d").strftime(
            '%Y-%m-%dT%H:%M:%S')
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
                    match_phrase = {"match_phrase": {"transaction.host_ip": ip}}
                    sp_param["bool"]["should"].append(match_phrase)
                es_result = self.sear_info(st_time, ed_time, sp_param)
                return HttpResponse(es_result)
            except Exception as err:
                print(err)
                return HttpResponse("Error")

    def post(self, request):
        time = request.POST['tim']
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
        if time == 'None':
            st_time = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d").strftime(
                '%Y-%m-%dT%H:%M:%S')
        else:
            st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-int(time))).strftime('%Y-%m-%dT%H:%M:00')
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
                    match_phrase = {"match_phrase": {"transaction.host_ip": ip}}
                    sp_param["bool"]["should"].append(match_phrase)
                es_result = self.sear_info(st_time, ed_time, sp_param)
                return HttpResponse(es_result)
            except Exception as err:
                print(err)
                return HttpResponse("Error")

    def sear_info(self, st_time, ed_time, sp_param):
        if sp_param == None:
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
        else:
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
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-1)).strftime('%Y-%m-%dT%H:%M:00')
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
        time = int(request.POST['edtime'])
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-time)).strftime('%Y-%m-%dT%H:%M:00')
        if request.POST.get('comid'):
            comid = int(request.POST.get('comid'))
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
                    match_phrase = {"match_phrase": {"dst_ip.ip": ip}}
                    sp_param["bool"]["should"].append(match_phrase)
                es_result = self.sear_info(st_time, ed_time, sp_param)
                return HttpResponse(es_result)
            except Exception as err:
                print(err)
                return HttpResponse("Error")

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
        except Exception as err:
            logger.error('获取攻击top数据出错：{}'.format(err))
            return False


# 风险占比
class Safety_risk(View):

    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区是按 秒和毫秒为整数
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-1)).strftime('%Y-%m-%dT%H:%M:00')
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
        time = int(request.POST['edtime'])
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-time)).strftime('%Y-%m-%dT%H:%M:00')
        if request.POST.get('comid'):
            comid = int(request.POST.get('comid'))
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
                    match_phrase = {"match_phrase": {"dst_ip.ip": ip}}
                    sp_param["bool"]["should"].append(match_phrase)
                es_result = self.sear_info(st_time, ed_time, sp_param)
                return HttpResponse(es_result)
            except Exception as err:
                print(err)
                return HttpResponse("Error")

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
        except Exception as err:
            logger.error('获取风险占比数据出错：{}'.format(err))
            return False


# 主要受攻击端口占比
class Safety_attack_port(View):

    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区是按 秒和毫秒为整数
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-1)).strftime('%Y-%m-%dT%H:%M:00')
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
        time = int(request.POST['edtime'])
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-time)).strftime('%Y-%m-%dT%H:%M:00')
        if request.POST.get('comid'):
            comid = int(request.POST.get('comid'))
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
                    match_phrase = {"match_phrase": {"dst_ip.ip": ip}}
                    sp_param["bool"]["should"].append(match_phrase)
                es_result = self.sear_info(st_time, ed_time, sp_param)
                return HttpResponse(es_result)
            except Exception as err:
                print(err)
                return HttpResponse("Error")

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
        except Exception as err:
            logger.error('获取端口数据出错：{}'.format(err))
            return False


# web安全威胁统计
class Safety_waf_attack_count(View):

    def get(self, request):
        comid = request.GET.get('comid', 'None')
        if comid == 'None':
            comid = None
        else:
            comid = int(comid)
        # comid = request.GET.get('comid', 0)  #企业ID
        time = int(request.GET.get('edtime', 0))
        if time == 0:
            result = self.seardat(comid)
        else:
            result = self.seardate(comid, time)
        res = result["dat"]
        # res = result.get('dat','')
        paginator = Paginator(res, 4)  # 分页功能，一页8条数据
        if request.is_ajax() == False:
            userlist = paginator.page(1)
            content = {
                "compid": comid,
                "users": userlist
            }
            return JsonResponse(content)
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
            user_li = list(users)  # .object_list.values()
            # 分别为是否有上一页false/true，是否有下一页false/true，总共多少页，当前页面的数据
            result = {'has_previous': users.has_previous(),
                      'has_next': users.has_next(),
                      'num_pages': users.paginator.num_pages,
                      'user_li': user_li,
                      'now_page': page, }
            return JsonResponse(result)

    def seardat(self, comid):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区是按 秒和毫秒为整数
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-7)).strftime('%Y-%m-%dT%H:%M:00')
        # 获取
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
                    match_phrase = {"match_phrase": {"transaction.host_ip.keyword": ip}}
                    sp_param["bool"]["should"].append(match_phrase)
                self.es_result = self.sear_info(st_time, ed_time, sp_param)
                return self.es_result
            except Exception as err:
                print(err)
                return False

    def seardate(self, comid, time):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区时间
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-time)).strftime('%Y-%m-%dT%H:%M:00')
        # 获取
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
                    match_phrase = {"match_phrase": {"transaction.host_ip.keyword": ip}}
                    sp_param["bool"]["should"].append(match_phrase)
                self.es_result = self.sear_info(st_time, ed_time, sp_param)
                return self.es_result
            except Exception as err:
                print(err)
                return False

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
            jsonlist, jsontext = [], {}
            for i in re_data:  # 多个
                buck_a = i['3']['buckets']
                for v in buck_a:  # 多个
                    try:
                        jsontext_1 = {}
                        # 遍历数据
                        buck_b = v['4']['buckets']
                        y_id = v['key']  # 源IP
                        y_count = v['doc_count']  # 数量
                        jsontext_1["y_id"] = y_id
                        jsontext_1["y_count"] = y_count
                        for k in buck_b:
                            jsontext_1["w_type"] = k['key']  # 威胁情报类型
                            buck_c = k['5']['buckets']
                            for c in buck_c:
                                waf_ym = c['key']  # 域名
                                jsontext_1["waf_ym"] = waf_ym
                                buck_d = c['6']['buckets']
                                for d in buck_d:
                                    buck_d = d['7']['buckets']
                                    for l in buck_d:
                                        waf_lj = l['key']
                                        jsontext_1["waf_lj"] = waf_lj  # waf拦截器
                        jsonlist.append(jsontext_1)
                    except Exception as err:
                        logger.error('威胁分类数据报错：{}'.format(err))
                    continue
            jsontext['dat'] = jsonlist
            return jsontext
        except Exception as err:
            logger.error('威胁统计-数据-获取数据出错：{}'.format(err))
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)
