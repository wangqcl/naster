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
    port=9200,
    timeout=30,
    retry_on_timeout=True
)

class thindex(View):
    @check_user_request
    def get(self, request):
        comid = request.GET.get('comid',None)
        # result =self.seardat(comid)
        # res = result['dat']
        # paginator = Paginator(res, 8)    #分页功能，一页8条数据

        # if request.is_ajax() ==False:
        username = request.session.get('webuser', default=None)  # 获取登录用户名
        user = Users.objects.get(username=username)
        # userlist = paginator.page(1)
        paglist = [{"pag":1},{"pag":2},{"pag":3},{"pag":4},{"pag":5}]
        print(type(paglist))
        content = {
            "compid":comid,
            "paglist":paglist
        }
        if user.state == 0:
            if int(comid) == 0:
                return render(request, "web/threaten.html", content)
            else:
                return render(request, "web/usermon/qthreaten.html", content)
        elif user.state == 1 & int(comid) != 0:
            comp = Compinfo.objects.get(id=comid)
            users = comp.users.all()
            for us in users:
                if us.username == username:
                    return render(request, "web/usermon/qthreaten.html", content)  # 用户的监控首页
                else:
                    content = {"info": "查询失败！"}
            return render(request, "web/monweb/info.html", content)
        else:
            error = "访问出错！"
            content = {"info": error}
            return render(request, "web/monweb/info.html", content)

        # Ajax数据交互
        # if request.is_ajax():
        #     page = request.GET.get('page')
        #     try:
        #         users = paginator.page(page)
        #     # 如果页数不是整数，返回第一页
        #     except PageNotAnInteger:
        #         users = paginator.page(1)
        #     # 如果页数不存在/不合法，返回最后一页
        #     except InvalidPage:
        #         users = paginator.page(paginator.num_pages)
        #     user_li = list(users)  #.object_list.values()
        #     # 分别为是否有上一页false/true，是否有下一页false/true，总共多少页，当前页面的数据
        #     result = {'has_previous': users.has_previous(),
        #               'has_next': users.has_next(),
        #               'num_pages': users.paginator.num_pages,
        #               'user_li': user_li}
        #     return JsonResponse(result)
    # def seardat(self,comid):
    #     ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区是按 秒和毫秒为整数
    #     st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-1)).strftime('%Y-%m-%dT%H:%M:00')
    #     if int(comid) == 0:  # 是否携带用户信息
    #         sp_param = None
    #         es_result = self.sear_info(st_time, ed_time, sp_param)
    #         return es_result
    #     else:
    #         try:
    #             comp = Compinfo.objects.get(id=comid)
    #             comp_ip = comp.comp_ip  # IP
    #             comp_s = comp_ip.split(';')
    #             sp_param = {
    #                 "bool": {
    #                     "should": [
    #                     ],
    #                     "minimum_should_match": 1
    #                 }
    #             }
    #             for ip in comp_s:
    #                 match_phrase = {"match_phrase": {"dst_ip.ip": ip}}
    #                 sp_param["bool"]["should"].append(match_phrase)
    #             self.es_result = self.sear_info(st_time, ed_time, sp_param)
    #             if self.es_result == False:
    #                 return False
    #             else:
    #                 return self.es_result
    #         except Exception as err:
    #             logger.error('请求出错：{}'.format(err))
    #             return False
    #
    # def sear_info(self,st_time,ed_time,sp_param):
    #     if sp_param == None:
    #         body = {
    #           "version": "true",
    #           "size": 50,
    #           "sort": [
    #             {
    #               "@timestamp": {
    #                 "order": "desc",
    #                 "unmapped_type": "boolean"
    #               }
    #             }
    #           ],
    #           "_source": {
    #             "excludes": []
    #           },
    #           "stored_fields": [
    #             "*"
    #           ],
    #           "script_fields": {},
    #           "docvalue_fields": [
    #             {
    #               "field": "@timestamp",
    #               "format": "date_time"
    #             },
    #             {
    #               "field": "dst_ip.information.reputation.timestamp",
    #               "format": "date_time"
    #             },
    #             {
    #               "field": "src_ip.information.reputation.timestamp",
    #               "format": "date_time"
    #             }
    #           ],
    #           "query": {
    #             "bool": {
    #               "must": [],
    #               "filter": [
    #                 {
    #                   "match_all": {}
    #                 },
    #                 {
    #                   "match_all": {}
    #                 },
    #                 {
    #                   "range": {
    #                     "@timestamp": {
    #                       "format": "strict_date_optional_time",
    #                       "gte": st_time,
    #                       "lte": ed_time
    #                     }
    #                   }
    #                 }
    #               ],
    #               "should": [],
    #               "must_not": []
    #             }
    #           },
    #           "highlight": {
    #             "pre_tags": [
    #               "@kibana-highlighted-field@"
    #             ],
    #             "post_tags": [
    #               "@/kibana-highlighted-field@"
    #             ],
    #             "fields": {
    #               "*": {}
    #             },
    #             "fragment_size": 2147483647
    #           }
    #         } #全部
    #     else:
    #         body = {
    #           "version": "true",
    #           "size": 50,
    #           "sort": [
    #             {
    #               "@timestamp": {
    #                 "order": "desc",
    #                 "unmapped_type": "boolean"
    #               }
    #             }
    #           ],
    #           "_source": {
    #             "excludes": []
    #           },
    #           "stored_fields": [
    #             "*"
    #           ],
    #           "script_fields": {},
    #           "docvalue_fields": [
    #             {
    #               "field": "@timestamp",
    #               "format": "date_time"
    #             },
    #             {
    #               "field": "dst_ip.information.reputation.timestamp",
    #               "format": "date_time"
    #             },
    #             {
    #               "field": "src_ip.information.reputation.timestamp",
    #               "format": "date_time"
    #             }
    #           ],
    #           "query": {
    #             "bool": {
    #               "must": [],
    #               "filter": [
    #                 {
    #                   "match_all": {}
    #                 },
    #                 {
    #                   "match_all": {}
    #                 },
    #                 sp_param,
    #                 {
    #                   "range": {
    #                     "@timestamp": {
    #                       "format": "strict_date_optional_time",
    #                       "gte": st_time,
    #                       "lte": ed_time
    #                     }
    #                   }
    #                 }
    #               ],
    #               "should": [],
    #               "must_not": []
    #             }
    #           },
    #           "highlight": {
    #             "pre_tags": [
    #               "@kibana-highlighted-field@"
    #             ],
    #             "post_tags": [
    #               "@/kibana-highlighted-field@"
    #             ],
    #             "fields": {
    #               "*": {}
    #             },
    #             "fragment_size": 2147483647
    #           }
    #         } #按IP筛选
    #     try:
    #         ret = es.search(index='threat', doc_type='_doc', body=body)
    #         re_data = ret['hits']['hits']
    #         datalist = []
    #         for i in re_data:
    #             try:
    #                 e_dict = {}
    #                 time = i['_source']['@timestamp'].replace("T", " ")[:-16]
    #                 e_dict['time'] = time  #time
    #                 e_dict['src_ip'] = i['_source']['src_ip']['ip']  # Ip
    #                 e_dict['geo'] = i['_source']['src_ip']['information']['geo']  # geo
    #                 e_dict['tag'] = i['_source']['src_ip']['information']['reputation']['tag']   #tag
    #                 datalist.append(e_dict)
    #             except Exception as err:
    #                 logger.error('解析威胁情报详细数据报错：{}'.format(err))
    #             continue
    #         jstext = {}
    #         jstext['dat'] = datalist
    #         return jstext
    #     except Exception as err:
    #         logger.error('威胁情报-数据-获取数据出错：{}'.format(err))
    #         return False

class thattack(View):
    @check_user_request
    def get(self,request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区是按 秒和毫秒为整数
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-1)).strftime('%Y-%m-%dT%H:%M:00')
        #获取
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
                sp_param ={
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
                if es_result == False:
                    return HttpResponse("request false", status=404)
                else:
                    return HttpResponse(es_result)
            except Exception as err:
                logger.error('请求出错：{}'.format(err))
                return HttpResponse("request error", status=404)
    def post(self,request):
        info = {"请求失败！"}
        return HttpResponse(info)

    def sear_info(self,st_time,ed_time,sp_param):
        if sp_param == None:
            body = {
              "aggs": {
                "2": {
                  "terms": {
                    "field": "src_ip.information.reputation.tag.keyword",
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
            } #全部
        else:
            body = {
              "aggs": {
                "2": {
                  "terms": {
                    "field": "src_ip.information.reputation.tag.keyword",
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
            } #按IP筛选
        try:
            ret = es.search(index='threat', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            ports, number, jsontext = [], [], {}
            for i in re_data:
                number_dict = {}
                if i['key'] == "":
                    continue
                else:
                    ports.append(i['key'])
                    number_dict['name'],number_dict['value'] =  i['key'],i['doc_count']
                    number.append(number_dict)
            jsontext['ports'] = ports
            jsontext['number'] = number
            jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except Exception as err:
            logger.error('获取数据出错：{}'.format(err))
            return False

#命中趋势
class thhit(View):
    @check_user_request
    def get(self,request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区是按 秒和毫秒为整数
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-1)).strftime('%Y-%m-%dT%H:%M:00')
        #获取
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
                sp_param ={
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
                if es_result == False:
                    return HttpResponse("request false", status=404)
                else:
                    return HttpResponse(es_result)
            except Exception as err:
                logger.error('请求出错：{}'.format(err))
                return HttpResponse("request error", status=404)
    def post(self,request):
        info = {"请求失败！"}
        return HttpResponse(info)

    def sear_info(self,st_time,ed_time,sp_param):
        if sp_param == None:
            body = {
              "aggs": {
                "2": {
                  "date_histogram": {
                    "field": "@timestamp",
                    "fixed_interval": "30m",
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
            } #全部
        else:
            body = {
              "aggs": {
                "2": {
                  "date_histogram": {
                    "field": "@timestamp",
                    "fixed_interval": "30m",
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
            } #按IP筛选
        try:
            ret = es.search(index='threat', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            timelist, number, jsontext = [], [], {}
            for i in re_data:
                time = i['key_as_string'].replace("T", " ")[11:-13]
                timelist.append(time)
                number.append(i['doc_count'])
            jsontext['times'] = timelist
            jsontext['number'] = number
            jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except Exception as err:
            logger.error('获取数据出错：{}'.format(err))
            return False

#活跃攻击源
class thactive(View):
    @check_user_request
    def get(self,request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区是按 秒和毫秒为整数
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-1)).strftime('%Y-%m-%dT%H:%M:00')
        #获取
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
                sp_param ={
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
                if es_result == False:
                    return HttpResponse("request false", status=404)
                else:
                    return HttpResponse(es_result)
            except Exception as err:
                logger.error('请求出错：{}'.format(err))
                return HttpResponse("request error", status=404)
    def post(self,request):
        info = {"请求失败！"}
        return HttpResponse(info)

    def function(self,date):
        return date['doc_count']

    def sear_info(self,st_time,ed_time,sp_param):
        if sp_param == None:
            body = {
              "aggs": {
                "2": {
                  "terms": {
                    "field": "src_ip.ip.keyword",
                    "order": {
                      "_count": "desc"
                    },
                    "size": 10
                  },
                  "aggs": {
                    "3": {
                      "terms": {
                        "field": "src_ip.ip.keyword",
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
            } #全部
        else:
            body = {
              "aggs": {
                "2": {
                  "terms": {
                    "field": "src_ip.ip.keyword",
                    "order": {
                      "_count": "desc"
                    },
                    "size": 10
                  },
                  "aggs": {
                    "3": {
                      "terms": {
                        "field": "src_ip.ip.keyword",
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
            } #按IP筛选
        try:
            ret = es.search(index='threat', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            allbuck,jsontext = [],{}
            for i in re_data:
                bucklist = {}
                bucklist["key"] = i["key"]
                bucklist["doc_count"] = i["doc_count"]
                allbuck.append(bucklist)
            x_data,y_data = [],[]
            allbuck.sort(key=self.function)
            for da in allbuck:
                x_data.append(da["key"])
                y_data.append(da["doc_count"])
            jsontext['x_data'] = x_data
            jsontext['y_data'] = y_data
            jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except Exception as err:
            logger.error('获取数据出错：{}'.format(err))
            return False

#IP威胁分类
class threat(View):
    @check_user_request
    def get(self,request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区是按 秒和毫秒为整数
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-1)).strftime('%Y-%m-%dT%H:%M:00')
        #获取
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
                sp_param ={
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
                if es_result == False:
                    return HttpResponse("request false", status=404)
                else:
                    return HttpResponse(es_result)
            except Exception as err:
                logger.error('请求出错：{}'.format(err))
                return HttpResponse("request error", status=404)
    def post(self,request):
        info = {"请求失败！"}
        return HttpResponse(info)

    def sear_info(self,st_time,ed_time,sp_param):
        if sp_param == None:
            body = {
              "aggs": {
                "2": {
                  "terms": {
                    "field": "src_ip.ip.keyword",
                    "order": {
                      "_count": "desc"
                    },
                    "size": 10
                  },
                  "aggs": {
                    "3": {
                      "terms": {
                        "field": "src_ip.information.reputation.category.keyword",
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
            } #全部
        else:
            body = {
              "aggs": {
                "2": {
                  "terms": {
                    "field": "src_ip.ip.keyword",
                    "order": {
                      "_count": "desc"
                    },
                    "size": 10
                  },
                  "aggs": {
                    "3": {
                      "terms": {
                        "field": "src_ip.information.reputation.category.keyword",
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
            } #按IP筛选
        try:
            ret = es.search(index='threat', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            n_name,n_data,w_data,jsontext = [],[],[],{}
            for i in re_data:
                n_data_j = {}
                n_name.append(i["key"])

                n_data_j["name"] = i["key"]
                n_data_j["value"] = i["doc_count"]
                n_data.append(n_data_j)
                bucklist = i["3"]["buckets"]

                for v in bucklist:
                    w_data_j = {}
                    w_data_j["name"] = v["key"]
                    w_data_j["value"] = v["doc_count"]
                    w_data.append(w_data_j)

            jsontext['n_name'] = n_name
            jsontext['n_data'] = n_data
            jsontext['w_data'] = w_data
            jsontext['edtime'] = ed_time

            return json.dumps(jsontext)
        except Exception as err:
            logger.error('获取数据出错：{}'.format(err))
            return False

#IP威胁情报源
class thnews(View):
    @check_user_request
    def get(self,request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区是按 秒和毫秒为整数
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-1)).strftime('%Y-%m-%dT%H:%M:00')
        #获取
        comid = request.GET.get('comid', None)
        if comid == None:  # 是否携带用户信息
            sp_param = None
            es_result = self.sear_info(st_time, ed_time, sp_param)
            if es_result == False:
                return HttpResponse("request false", status=404)
            else:
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
                    match_phrase = {"match_phrase": {"dst_ip.ip": ip}}
                    sp_param["bool"]["should"].append(match_phrase)
                es_result = self.sear_info(st_time, ed_time, sp_param)
                if es_result == False:
                    return HttpResponse("request false", status=404)
                else:
                    return HttpResponse(es_result)
            except Exception as err:
                logger.error('请求出错：{}'.format(err))
                return HttpResponse("request error",status=404)

    def post(self,request):
        info = {"请求失败！"}
        return HttpResponse(info)

    def sear_info(self,st_time,ed_time,sp_param):
        if sp_param == None:
            body = {
              "aggs": {
                "2": {
                  "terms": {
                    "field": "src_ip.ip.keyword",
                    "order": {
                      "_count": "desc"
                    },
                    "size": 10
                  },
                  "aggs": {
                    "3": {
                      "terms": {
                        "field": "src_ip.information.reputation.source_ref.keyword",
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
            } #全部
        else:
            body = {
              "aggs": {
                "2": {
                  "terms": {
                    "field": "src_ip.ip.keyword",
                    "order": {
                      "_count": "desc"
                    },
                    "size": 10
                  },
                  "aggs": {
                    "3": {
                      "terms": {
                        "field": "src_ip.information.reputation.source_ref.keyword",
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
            } #按IP筛选
        try:
            ret = es.search(index='threat', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            n_name,n_data,w_data,jsontext = [],[],[],{}
            for i in re_data:
                n_data_j = {}
                n_name.append(i["key"])

                n_data_j["name"] = i["key"]
                n_data_j["value"] = i["doc_count"]
                n_data.append(n_data_j)
                bucklist = i["3"]["buckets"]

                for v in bucklist:
                    w_data_j = {}
                    w_data_j["name"] = v["key"]
                    w_data_j["value"] = v["doc_count"]
                    w_data.append(w_data_j)

            jsontext['n_name'] = n_name
            jsontext['n_data'] = n_data
            jsontext['w_data'] = w_data
            # jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except Exception as err:
            logger.error('获取数据出错：{}'.format(err))
            return False

class threaten_count(View):
    '''首页-web安全信息'''
    @check_user_request
    def get(self, request):
        comid = request.GET.get('comid', None)
        result = self.seardat(comid)
        res = result['dat']
        paginator = Paginator(res, 8)  # 分页功能，一页8条数据
        if request.is_ajax() == False:
            userlist = paginator.page(1)
            content = {
                "compid": comid,
                "users": userlist
            }
            return JsonResponse(content)
            # Ajax数据交互
        if request.is_ajax():
            # print("调用了ajax请求")
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
                      'user_li': user_li}
            return JsonResponse(result)

    def seardat(self,comid):
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
                logger.error('请求出错：{}'.format(err))
                return False

    def sear_info(self,st_time,ed_time,sp_param):
        if sp_param == None:
            body = {
              "version": "true",
              "size": 40,
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
            } #全部
        else:
            body = {
              "version": "true",
              "size": 40,
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
            } #按IP筛选
        try:
            ret = es.search(index='threat', doc_type='_doc', body=body)
            re_data = ret['hits']['hits']
            datalist = []
            for i in re_data:
                try:
                    e_dict = {}
                    time = i['_source']['@timestamp'].replace("T", " ")[:-16]
                    e_dict['time'] = time  #time
                    e_dict['src_ip'] = i['_source']['src_ip']['ip']  # Ip
                    e_dict['geo'] = i['_source']['src_ip']['information']['geo']  # geo
                    e_dict['tag'] = i['_source']['src_ip']['information']['reputation']['tag']   #tag
                    datalist.append(e_dict)
                except Exception as err:
                    logger.error('解析威胁情报详细数据报错：{}'.format(err))
                continue
            jstext = {}
            jstext['dat'] = datalist
            return jstext
        except Exception as err:
            logger.error('威胁情报-数据-获取数据出错：{}'.format(err))
            return False




