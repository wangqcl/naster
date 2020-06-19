from django.shortcuts import render
from django.http import HttpResponse
from common.models import Users, Compinfo
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


# 监控首页
def index(request, pIndex=0):
    '''首页-全局监控信息'''
    username = request.session.get('webuser', default=None)  # 获取登录用户名
    user = Users.objects.get(username=username)
    if user.state == 0:
        if int(pIndex) == 0:
            content = {
                "compid": pIndex
            }
            return render(request, "web/monit.html", content)
        else:
            content = {
                "compid": pIndex
            }
            return render(request, "web/usermon/qsafety.html", content)  # 只查询此用户下的数据

    elif user.state == 1 or pIndex != 0:
        content = {
            "compid": pIndex
        }
        return render(request, "web/usermon/qsafety.html", content)  # 用户的监控首页
    else:
        error = "访问出错！"
        content = {"info": error}
        return render(request, "web/info.html", content)


# 请求数量
class Main_getnum(View):
    def get(self, request):
        comid = request.GET.get('comid', None)
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=-15)).strftime('%Y-%m-%dT%H:%M:00')
        if comid == None:  # 是否携带用户信息
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

    def post(self, request):
        st_time = request.POST['edtime']
        comid = request.POST['compid']
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
        if int(comid) == 0:  # 是否携带用户信息
            sp_param = None
            es_result = self.sear_info(st_time, ed_time, sp_param)
            return HttpResponse(es_result)
        else:
            comp = Compinfo.objects.get(id=comid)
            comp_ip = comp.comp_ip  # IP
            comp_realm = comp.comp_realm  # 域名

            if comp_ip != "" and comp_realm == "":  # Ip
                sp_param = "*%s*" % (comp_ip)
                es_result = self.sear_info(st_time, ed_time, sp_param)
                return HttpResponse(es_result)
            elif comp_ip != "" and comp_realm != "":  # 域名
                comp_s = comp_realm.split('.', 1)
                sp_param = "*%s*" % (comp_s[1])
                es_result = self.sear_info(st_time, ed_time, sp_param)
                return HttpResponse(es_result)
            else:
                return HttpResponse("Error")

    def sear_info(self, st_time, ed_time, sp_param):
        if sp_param == None:
            body = {
                "aggs": {
                    "2": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "calendar_interval": "1m",
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
            }  # 全部
        else:
            body = {
                "aggs": {
                    "2": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "calendar_interval": "1m",
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
            }  # 按域名筛选

        try:
            ret = es.search(index='logstash-nginx-log', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            tims, number, jsontext = [], [], {}
            for i in re_data:
                tims1 = i['key_as_string'].replace("T", " ")[11:-13]
                tims.append(tims1)
                number.append(i['doc_count'])
            jsontext['times'] = tims[:-1]
            jsontext['number'] = number[:-1]
            jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


# 主要访问端口
class Main_visit_port(View):

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
                            "field": "destination.port",
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
                    },
                    {
                        "field": "event.created",
                        "format": "date_time"
                    },
                    {
                        "field": "event.end",
                        "format": "date_time"
                    },
                    {
                        "field": "event.start",
                        "format": "date_time"
                    },
                    {
                        "field": "file.accessed",
                        "format": "date_time"
                    },
                    {
                        "field": "file.created",
                        "format": "date_time"
                    },
                    {
                        "field": "file.ctime",
                        "format": "date_time"
                    },
                    {
                        "field": "file.mtime",
                        "format": "date_time"
                    },
                    {
                        "field": "process.start",
                        "format": "date_time"
                    },
                    {
                        "field": "tls.client_certificate.not_after",
                        "format": "date_time"
                    },
                    {
                        "field": "tls.client_certificate.not_before",
                        "format": "date_time"
                    },
                    {
                        "field": "tls.server_certificate.not_after",
                        "format": "date_time"
                    },
                    {
                        "field": "tls.server_certificate.not_before",
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
            }  # 全部
        else:
            body = {
                "aggs": {
                    "2": {
                        "terms": {
                            "field": "destination.port",
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
                    },
                    {
                        "field": "event.created",
                        "format": "date_time"
                    },
                    {
                        "field": "event.end",
                        "format": "date_time"
                    },
                    {
                        "field": "event.start",
                        "format": "date_time"
                    },
                    {
                        "field": "file.accessed",
                        "format": "date_time"
                    },
                    {
                        "field": "file.created",
                        "format": "date_time"
                    },
                    {
                        "field": "file.ctime",
                        "format": "date_time"
                    },
                    {
                        "field": "file.mtime",
                        "format": "date_time"
                    },
                    {
                        "field": "process.start",
                        "format": "date_time"
                    },
                    {
                        "field": "tls.client_certificate.not_after",
                        "format": "date_time"
                    },
                    {
                        "field": "tls.client_certificate.not_before",
                        "format": "date_time"
                    },
                    {
                        "field": "tls.server_certificate.not_after",
                        "format": "date_time"
                    },
                    {
                        "field": "tls.server_certificate.not_before",
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
            }  # 按域名筛选
        try:
            ret = es.search(index='packetbeat-*', doc_type='_doc', body=body)
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


# 服务器状态码
class Server_status_code(View):
    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区是按 秒和毫秒为整数
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=-15)).strftime('%Y-%m-%dT%H:%M:00')
        comid = request.GET.get('comid', None)
        if comid == None:  # 是否携带用户信息
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
                            "fixed_interval": "5s",
                            "time_zone": "Asia/Shanghai",
                            "min_doc_count": 1
                        },
                        "aggs": {
                            "3": {
                                "terms": {
                                    "field": "status.keyword",
                                    "order": {
                                        "_count": "desc"
                                    },
                                    "size": 2
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
            }  # 全部
        else:
            body = {
                "aggs": {
                    "2": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "fixed_interval": "5s",
                            "time_zone": "Asia/Shanghai",
                            "min_doc_count": 1
                        },
                        "aggs": {
                            "3": {
                                "terms": {
                                    "field": "status.keyword",
                                    "order": {
                                        "_count": "desc"
                                    },
                                    "size": 2
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
            }  # 按域名筛选
        try:
            ret = es.search(index='logstash-nginx-log', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            list_date, jsontext, yAxis_data = [], {}, {}
            doc_count = []
            for i in re_data:
                list_date.append(i["key_as_string"][11:-13])  # 日期
                ret_buckets = i["3"]["buckets"]
                for v in ret_buckets:
                    port_key = v["key"]  # 端口
                    doc_count = v["doc_count"]  # 端口数量

                    # 判断jsontext中是否存在相同的key,端口
                    keys = list(yAxis_data.keys())
                    if (port_key in keys):
                        if len(yAxis_data[port_key]) < len(list_date) - 1:
                            diff = len(list_date) - len(yAxis_data[port_key])
                            diff_list = ['' for _ in range(diff - 1)]
                            yAxis_data[port_key].extend(diff_list)  # 合并补空位
                            yAxis_data[port_key].append(doc_count)
                        # 继续添加
                        else:
                            yAxis_data[port_key].append(doc_count)
                    else:
                        # 新加
                        null_list = ['' for _ in range(len(list_date) - 1)]
                        yAxis_data.setdefault(port_key, null_list).append(doc_count)  # 添加端口和数量
                jsontext['yAxis'] = yAxis_data  # 端口对应数据量
                jsontext['xAxis'] = list_date  # X轴
                jsontext['port'] = list(yAxis_data.keys())  # 所有端口值
            return json.dumps(jsontext)
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


# 域名被访问次数
class Domain_infor(View):
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
                            "calendar_interval": "1m",
                            "time_zone": "Asia/Shanghai",
                            "min_doc_count": 1
                        },
                        "aggs": {
                            "3": {
                                "terms": {
                                    "field": "domain.keyword",
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
                        "date_histogram": {
                            "field": "@timestamp",
                            "calendar_interval": "1m",
                            "time_zone": "Asia/Shanghai",
                            "min_doc_count": 1
                        },
                        "aggs": {
                            "3": {
                                "terms": {
                                    "field": "domain.keyword",
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
            }  # 按域名筛选
        try:
            ret = es.search(index='logstash-nginx-log', doc_type='_doc', body=body)
            print(ret)
            re_data = ret['aggregations']['2']['buckets']
            list_date, jsontext, yAxis_data = [], {}, {}
            doc_count = []
            for i in re_data:
                list_date.append(i["key_as_string"][11:-13])  # 获取日期数据并放入列表
                ret_buckets = i["3"]["buckets"]
                for v in ret_buckets:
                    port_key = v["key"]  # 端口
                    print(port_key)
                    doc_count = v["doc_count"]  # 获取端口对应数量
                    print(doc_count)
                    # 判断jsontext中是否存在相同的key,端口
                    keys = list(yAxis_data.keys())
                    if (port_key in keys):
                        # print("存在")
                        if len(yAxis_data[port_key]) < len(list_date) - 1:

                            diff = len(list_date) - len(yAxis_data[port_key])
                            diff_list = ['0' for _ in range(diff - 1)]
                            yAxis_data[port_key].extend(diff_list)  # 合并补空位
                            yAxis_data[port_key].append(doc_count)
                        # 如果存在继续添加
                        else:
                            yAxis_data[port_key].append(doc_count)
                    else:

                        null_list = ['0' for _ in range(len(list_date) - 1)]
                        yAxis_data.setdefault(port_key, null_list).append(doc_count)  # 字典中添加端口和数量
                jsontext['yAxis'] = yAxis_data  # 域名对应数据量
                jsontext['xAxis'] = list_date[:-1]  # 日期列表做X轴
                jsontext['port'] = list(yAxis_data.keys())  # 统计所有域名
                # jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


# 主要IP分值
class Ip_fraction(View):
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
                            "field": "src_ip.keyword",
                            "order": {
                                "1": "desc"
                            },
                            "size": 10
                        },
                        "aggs": {
                            "1": {
                                "avg": {
                                    "field": "score"
                                }
                            },
                            "3": {
                                "terms": {
                                    "field": "src_ip.keyword",
                                    "order": {
                                        "1": "desc"
                                    },
                                    "size": 10
                                },
                                "aggs": {
                                    "1": {
                                        "avg": {
                                            "field": "score"
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
                        "field": "timestamp",
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
                                    "timestamp": {
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
                            "field": "src_ip.keyword",
                            "order": {
                                "1": "desc"
                            },
                            "size": 10
                        },
                        "aggs": {
                            "1": {
                                "avg": {
                                    "field": "score"
                                }
                            },
                            "3": {
                                "terms": {
                                    "field": "src_ip.keyword",
                                    "order": {
                                        "1": "desc"
                                    },
                                    "size": 10
                                },
                                "aggs": {
                                    "1": {
                                        "avg": {
                                            "field": "score"
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
                        "field": "timestamp",
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
                                    "timestamp": {
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
            ret = es.search(index='total', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            ports, number, jsontext = [], [], {}
            for i in re_data:
                ports.append(i['key'])  # 域名
                ip_frac = i['1']['value']
                number.append(round(ip_frac))  # 分值,四舍五入
            jsontext['ports'] = ports
            jsontext['number'] = number
            jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


# 客户端请求流量
class Request_traffic(View):
    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
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
                    "3": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "fixed_interval": "30s",
                            "time_zone": "Asia/Shanghai",
                            "min_doc_count": 1
                        },
                        "aggs": {
                            "4": {
                                "terms": {
                                    "field": "source.ip",
                                    "order": {
                                        "1": "desc"
                                    },
                                    "size": 3
                                },
                                "aggs": {
                                    "1": {
                                        "sum": {
                                            "field": "source.bytes"
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
                        "field": "event.created",
                        "format": "date_time"
                    },
                    {
                        "field": "event.end",
                        "format": "date_time"
                    },
                    {
                        "field": "event.start",
                        "format": "date_time"
                    },
                    {
                        "field": "file.accessed",
                        "format": "date_time"
                    },
                    {
                        "field": "file.created",
                        "format": "date_time"
                    },
                    {
                        "field": "file.ctime",
                        "format": "date_time"
                    },
                    {
                        "field": "file.mtime",
                        "format": "date_time"
                    },
                    {
                        "field": "process.start",
                        "format": "date_time"
                    },
                    {
                        "field": "tls.client_certificate.not_after",
                        "format": "date_time"
                    },
                    {
                        "field": "tls.client_certificate.not_before",
                        "format": "date_time"
                    },
                    {
                        "field": "tls.server_certificate.not_after",
                        "format": "date_time"
                    },
                    {
                        "field": "tls.server_certificate.not_before",
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
        else:
            body = {
                "aggs": {
                    "3": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "fixed_interval": "30s",
                            "time_zone": "Asia/Shanghai",
                            "min_doc_count": 1
                        },
                        "aggs": {
                            "4": {
                                "terms": {
                                    "field": "source.ip",
                                    "order": {
                                        "1": "desc"
                                    },
                                    "size": 3
                                },
                                "aggs": {
                                    "1": {
                                        "sum": {
                                            "field": "source.bytes"
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
                        "field": "event.created",
                        "format": "date_time"
                    },
                    {
                        "field": "event.end",
                        "format": "date_time"
                    },
                    {
                        "field": "event.start",
                        "format": "date_time"
                    },
                    {
                        "field": "file.accessed",
                        "format": "date_time"
                    },
                    {
                        "field": "file.created",
                        "format": "date_time"
                    },
                    {
                        "field": "file.ctime",
                        "format": "date_time"
                    },
                    {
                        "field": "file.mtime",
                        "format": "date_time"
                    },
                    {
                        "field": "process.start",
                        "format": "date_time"
                    },
                    {
                        "field": "tls.client_certificate.not_after",
                        "format": "date_time"
                    },
                    {
                        "field": "tls.client_certificate.not_before",
                        "format": "date_time"
                    },
                    {
                        "field": "tls.server_certificate.not_after",
                        "format": "date_time"
                    },
                    {
                        "field": "tls.server_certificate.not_before",
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
        try:
            ret = es.search(index='packetbeat-*', doc_type='_doc', body=body)
            re_data = ret['aggregations']['3']['buckets']
            list_date, jsontext, yAxis_data = [], {}, {}
            for i in re_data:
                # 获取当前日期
                list_date.append(i["key_as_string"][11:-10])  # 日期
                ret_buckets = i["4"]["buckets"]
                for v in ret_buckets:
                    port_key = v["key"]  # IP
                    doc_count = round((v["1"]["value"] / 1024) * 100) / 100.0  # 流量
                    keys = list(yAxis_data.keys())
                    if (port_key in keys):
                        if len(yAxis_data[port_key]) < len(list_date) - 1:
                            diff = len(list_date) - len(yAxis_data[port_key])
                            diff_list = ['0' for _ in range(diff - 1)]
                            yAxis_data[port_key].extend(diff_list)  # 合并补空位
                            yAxis_data[port_key].append(doc_count)
                        else:
                            yAxis_data[port_key].append(doc_count)
                    else:
                        null_list = ['0' for _ in range(len(list_date) - 1)]
                        yAxis_data.setdefault(port_key, null_list).append(doc_count)
                jsontext['yAxis'] = yAxis_data  # 数据量
                jsontext['xAxis'] = list_date[:-1]  # 日期
                jsontext['port'] = list(yAxis_data.keys())  # 所有域名
                jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


# 客户端回应流量
class Response_traffic(View):
    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=-15)).strftime('%Y-%m-%dT%H:%M:00')
        es_result = self.sear_info(st_time, ed_time)
        return HttpResponse(es_result)

    def post(self, request):
        info = {"请求失败！"}
        return HttpResponse(info)

    def sear_info(self, st_time, ed_time):
        body = {
            "aggs": {
                "2": {
                    "date_histogram": {
                        "field": "@timestamp",
                        "fixed_interval": "30s",
                        "time_zone": "Asia/Shanghai",
                        "min_doc_count": 1
                    },
                    "aggs": {
                        "3": {
                            "terms": {
                                "field": "destination.ip",
                                "order": {
                                    "1": "desc"
                                },
                                "size": 5
                            },
                            "aggs": {
                                "1": {
                                    "sum": {
                                        "field": "destination.bytes"
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
                    "field": "event.created",
                    "format": "date_time"
                },
                {
                    "field": "event.end",
                    "format": "date_time"
                },
                {
                    "field": "event.start",
                    "format": "date_time"
                },
                {
                    "field": "file.accessed",
                    "format": "date_time"
                },
                {
                    "field": "file.created",
                    "format": "date_time"
                },
                {
                    "field": "file.ctime",
                    "format": "date_time"
                },
                {
                    "field": "file.mtime",
                    "format": "date_time"
                },
                {
                    "field": "process.start",
                    "format": "date_time"
                },
                {
                    "field": "tls.client_certificate.not_after",
                    "format": "date_time"
                },
                {
                    "field": "tls.client_certificate.not_before",
                    "format": "date_time"
                },
                {
                    "field": "tls.server_certificate.not_after",
                    "format": "date_time"
                },
                {
                    "field": "tls.server_certificate.not_before",
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
            ret = es.search(index='packetbeat-*', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            list_date, jsontext, yAxis_data = [], {}, {}
            for i in re_data:
                # 获取当前日期
                date = i["key_as_string"]
                list_date.append(date.replace("T", " ")[:-10])  # 日期
                ret_buckets = i["3"]["buckets"]

                for v in ret_buckets:
                    port_key = v["key"]  # IP
                    doc_count = round((v["1"]["value"] / 1048576) * 100) / 100.0  # 流量
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
                jsontext['xAxis'] = list_date[:-1]  # 日期
                jsontext['port'] = list(yAxis_data.keys())  # 所有域名
                jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


# waf攻击趋势
class Waf_attack_trend(View):
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


# 态势地图
class Attack_map(View):
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


# 接入状态 不启用
class Access_ip(View):
    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(minutes=-15)).strftime('%Y-%m-%dT%H:%M:00')
        es_result = self.sear_info(st_time, ed_time)
        print(es_result)
        return HttpResponse(es_result)

    def post(self, request):
        info = {"请求失败！"}
        return HttpResponse(info)

    def sear_info(self, st_time, ed_time):
        body = {
            "aggs": {
                "2": {
                    "date_range": {
                        "field": "@timestamp",
                        "ranges": [
                            {
                                "from": "now-1m",
                                "to": "now"
                            }
                        ],
                        "time_zone": "Asia/Shanghai"
                    },
                    "aggs": {
                        "3": {
                            "terms": {
                                "field": "状态.keyword",
                                "order": {
                                    "_count": "desc"
                                },
                                "size": 5
                            },
                            "aggs": {
                                "4": {
                                    "terms": {
                                        "field": "域名.keyword",
                                        "order": {
                                            "_count": "desc"
                                        },
                                        "size": 1000
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
                            "range": {
                                "@timestamp": {
                                    "format": "strict_date_optional_time",
                                    "gte": "2020-06-05T08:53:52.813Z",
                                    "lte": "2020-06-05T09:08:52.813Z"
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
            ret = es.search(index='flag*', doc_type='_doc', body=body)
            print(ret)
            re_data = ret['aggregations']['2']['buckets']
            jsontext = {}
            data1, data2 = [], []  # IP总数，#接入数据
            data1.append(re_data[0]["doc_count"])  # IP总数
            print(data1)
            # buck1 = re_data['3']['buckets']

            # print(re_data)
            # for i in re_data:
            #     print(i["3"]["buckets"])

            # for i in aa:
            #     #获取接入数据
            #     buck1 = {}
            #     buck1["name"] = i["key"]
            #     buck1["value"] = i["doc_count"]
            #     data2.append(buck1)
            #     bb = i["4"]["buckets"][0]
            #     for v in bb:
            #         buck2 = {}
            #         buck2["name"] = v["key"]
            #         buck2["value"] = v["doc_count"]
            #         data2.append(buck2)
            jsontext['edtime'] = ed_time
            # jsontext['data2'] = data2
            return json.dumps(jsontext, ensure_ascii=False)
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


# 今日命中数
class Hit(View):
    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
        st_time = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d").strftime(
            '%Y-%m-%dT%H:%M:%S')
        st_all_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-1)).strftime('%Y-%m-%dT%H:%M:00')  # 24小时
        num_today = self.Hit_day(st_time, ed_time)  # 今日命中
        num_all = self.Hit_all(st_all_time, ed_time)  # 全部命中
        jsontext = {}
        jsontext["num_today"] = num_today
        jsontext["num_all"] = num_all
        return HttpResponse(json.dumps(jsontext))

    def post(self, request):
        info = {"请求失败！"}
        return HttpResponse(info)

    def Hit_day(self, st_time, ed_time):
        body = {
            "aggs": {
                "2": {
                    "date_range": {
                        "field": "@timestamp",
                        "ranges": [
                            {
                                "from": "now-0d/d",
                                "to": "now"
                            }
                        ],
                        "time_zone": "Asia/Shanghai"
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
                    "field": "dst_ip.information.reputation.timestamp",
                    "format": "date_time"
                },
                {
                    "field": "src_ip.information.reputation.timestamp",
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
            ret = es.search(index='threat', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            for co in re_data:
                hit_day = co["doc_count"]
            return hit_day
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)

    def Hit_all(self, st_all_time, ed_time):
        # 24小时命中数
        body = {
            "aggs": {
                "2": {
                    "date_range": {
                        "field": "@timestamp",
                        "ranges": [
                            {
                                "from": "now-0d/d",
                                "to": "now"
                            }
                        ],
                        "time_zone": "Asia/Shanghai"
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
                    "field": "dst_ip.information.reputation.timestamp",
                    "format": "date_time"
                },
                {
                    "field": "src_ip.information.reputation.timestamp",
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
                                    "gte": st_all_time,
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
            ret = es.search(index='threat', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            for co in re_data:
                hit_all = co["doc_count"]
            return hit_all
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)


class Source_data(View):
    def get(self, request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-1)).strftime('%Y-%m-%dT%H:%M:00')
        es_result = self.sear_info(st_time, ed_time)
        # print(st_time)
        return HttpResponse(es_result)

    def post(self, request):
        info = {"请求失败！"}
        return HttpResponse(info)

    def sear_info(self, st_time, ed_time):
        body = {
            "aggs": {
                "3": {
                    "terms": {
                        "field": "source.ip",
                        "order": {
                            "1": "desc"
                        },
                        "size": 5
                    },
                    "aggs": {
                        "1": {
                            "sum": {
                                "field": "source.bytes"
                            }
                        },
                        "4": {
                            "terms": {
                                "field": "destination.ip",
                                "order": {
                                    "1": "desc"
                                },
                                "size": 5
                            },
                            "aggs": {
                                "1": {
                                    "sum": {
                                        "field": "source.bytes"
                                    }
                                },
                                "2": {
                                    "sum": {
                                        "field": "destination.bytes"
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
                    "field": "event.created",
                    "format": "date_time"
                },
                {
                    "field": "event.end",
                    "format": "date_time"
                },
                {
                    "field": "event.start",
                    "format": "date_time"
                },
                {
                    "field": "file.accessed",
                    "format": "date_time"
                },
                {
                    "field": "file.created",
                    "format": "date_time"
                },
                {
                    "field": "file.ctime",
                    "format": "date_time"
                },
                {
                    "field": "file.mtime",
                    "format": "date_time"
                },
                {
                    "field": "process.start",
                    "format": "date_time"
                },
                {
                    "field": "tls.client_certificate.not_after",
                    "format": "date_time"
                },
                {
                    "field": "tls.client_certificate.not_before",
                    "format": "date_time"
                },
                {
                    "field": "tls.server_certificate.not_after",
                    "format": "date_time"
                },
                {
                    "field": "tls.server_certificate.not_before",
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
            ret = es.search(index='packetbeat-*', doc_type='_doc', body=body)
            re_data = ret['aggregations']['3']['buckets']
            jsontext, datalist = {}, []
            for v in re_data:
                da_list = v["4"]["buckets"]
                for i in da_list:
                    data = []
                    data.append(v["key"])  # 源IP
                    data.append(i["key"])  # 目的IP
                    data.append(format(i["1"]["value"] / 1048576, '.2f'))  # 源数据
                    data.append(format(i["2"]["value"] / 1048576, '.2f'))  # 回应数据
                    datalist.append(data)
            print(datalist)
            jsontext['edtime'] = ed_time
            jsontext['data'] = datalist
            return json.dumps(jsontext, ensure_ascii=False)
        except:
            errinfo = {"error": "数据请求失败！"}
            return HttpResponse(errinfo)
