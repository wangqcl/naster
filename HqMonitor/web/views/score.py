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

#首页
class scindex(View):
    @check_user_request
    def get(self, request):
        comid = request.GET.get('comid',None)
        username = request.session.get('webuser', default=None)
        user = Users.objects.get(username=username)

        result = self.seardat(comid)
        res = result["dat"]
        if res != False:
            paginator = Paginator(res, 8)  # 分页功能，一页8条数据
            userlist = paginator.page(1)
            content = {
                "compid": comid,
                "users": userlist
            }
        else:
            content = {
                "compid": comid
            }

        if user.state == 0:
            if int(comid) == 0:
                return render(request, "web/score.html", content)
            else:
                return render(request, "web/usermon/qscore.html", content)
        elif user.state == 1 & int(comid) != 0:
            comp = Compinfo.objects.get(id=comid)
            users = comp.users.all()
            for us in users:
                if us.username == username:
                    return render(request, "web/usermon/qscore.html", content)  # 用户的监控首页
                else:
                    content = {"info": "查询失败！"}
            return render(request, "web/monweb/info.html", content)
        else:
            error = "访问出错！"
            content = {"info": error}
            return render(request, "web/monweb/info.html", content)

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
                    match_phrase = {"match_phrase": {"dst_ip": ip}}
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
              "aggs": {
                "2": {
                  "terms": {
                    "field": "src_ip.keyword",
                    "order": {
                      "_count": "desc"
                    },
                    "size": 10
                  },
                  "aggs": {
                    "3": {
                      "terms": {
                        "field": "dst_ip.keyword",
                        "order": {
                          "_count": "desc"
                        },
                        "size": 10
                      },
                      "aggs": {
                        "4": {
                          "terms": {
                            "field": "snort.type.keyword",
                            "order": {
                              "_count": "desc"
                            },
                            "size": 10
                          },
                          "aggs": {
                            "5": {
                              "terms": {
                                "field": "ti.type.keyword",
                                "order": {
                                  "_count": "desc"
                                },
                                "size": 10
                              },
                              "aggs": {
                                "6": {
                                  "terms": {
                                    "field": "waf.type.keyword",
                                    "order": {
                                      "_count": "desc"
                                    },
                                    "size": 10
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
            } #全部
        else:
            body = {
              "aggs": {
                "2": {
                  "terms": {
                    "field": "src_ip.keyword",
                    "order": {
                      "_count": "desc"
                    },
                    "size": 10
                  },
                  "aggs": {
                    "3": {
                      "terms": {
                        "field": "dst_ip.keyword",
                        "order": {
                          "_count": "desc"
                        },
                        "size": 10
                      },
                      "aggs": {
                        "4": {
                          "terms": {
                            "field": "snort.type.keyword",
                            "order": {
                              "_count": "desc"
                            },
                            "size": 10
                          },
                          "aggs": {
                            "5": {
                              "terms": {
                                "field": "ti.type.keyword",
                                "order": {
                                  "_count": "desc"
                                },
                                "size": 10
                              },
                              "aggs": {
                                "6": {
                                  "terms": {
                                    "field": "waf.type.keyword",
                                    "order": {
                                      "_count": "desc"
                                    },
                                    "size": 10
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
            } #按IP筛选
        try:
            ret = es.search(index='total', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            jsonlist = []
            for i in re_data:  #多个
                buck_a = i['3']['buckets']
                for v in buck_a:   #多个
                    try:
                        jsontext_1 = {}
                        #遍历数据
                        buck_b = v['4']['buckets']
                        y_id = v['key']    # 源IP
                        jsontext_1["y_id"] = y_id
                        number = v['doc_count']  #数量
                        jsontext_1["number"] = number
                        for k in buck_b:
                            m_ip = k['key']#目的IP
                            jsontext_1["m_ip"] = m_ip
                            buck_c = k['5']['buckets']
                            for c in buck_c:
                                w_ip = c['key']  # 威胁情报类型
                                jsontext_1["w_ip"] = w_ip
                                buck_d = c['6']['buckets']
                                for d in buck_d:
                                    waf_ip = d['key']  # waf类型
                                    jsontext_1["waf_ip"] = waf_ip
                        jsonlist.append(jsontext_1)
                    except Exception as err:
                        logger.error('威胁分类数据报错：{}'.format(err))
                    continue
            jstext = {}
            jstext['dat'] = jsonlist
            return jstext
        except Exception as err:
            logger.error('威胁情报-数据-获取数据出错：{}'.format(err))
            return False

#主要威胁IP分值
class mainthr(View):
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
                    match_phrase = {"match_phrase": {"dst_ip": ip}}
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
            } #全部
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
            } #按IP筛选
        try:
            ret = es.search(index='total', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            allbuck,jsontext = [],{}
            for i in re_data:
                bucklist = {}
                bucklist["key"] = i["key"]
                bucklist["doc_count"] = i["1"]["value"]
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

#总威胁趋势
class totalthr(View):
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
                    match_phrase = {"match_phrase": {"dst_ip": ip}}
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
        st_time = request.POST['edtime']
        comid = request.POST['compid']
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
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

    def sear_info(self,st_time,ed_time,sp_param):
        if sp_param == None:
            body = {
              "aggs": {
                "2": {
                  "date_histogram": {
                    "field": "timestamp",
                    "fixed_interval": "30m",
                    "time_zone": "Asia/Shanghai",
                    "min_doc_count": 1
                  },
                  "aggs": {
                    "1": {
                      "avg": {
                        "field": "score"
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
            } #全部
        else:
            body = {
              "aggs": {
                "2": {
                  "date_histogram": {
                    "field": "timestamp",
                    "fixed_interval": "30m",
                    "time_zone": "Asia/Shanghai",
                    "min_doc_count": 1
                  },
                  "aggs": {
                    "1": {
                      "avg": {
                        "field": "score"
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
            } #按IP筛选
        try:
            ret = es.search(index='total', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            tims, number, jsontext = [], [], {}
            for i in re_data:
                time1 = i["key_as_string"].replace("T", " ")[11:-13]
                tims.append(time1)
                value = i["1"]["value"]
                number.append(round(value,2))

            jsontext['times'] = tims[:-1]
            jsontext['number'] = number[:-1]
            jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except Exception as err:
            logger.error('获取数据出错：{}'.format(err))
            return False

#TI威胁趋势
class tithr(View):
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
                    match_phrase = {"match_phrase": {"dst_ip": ip}}
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
        st_time = request.POST['edtime']
        comid = request.POST['compid']
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
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

    def sear_info(self,st_time,ed_time,sp_param):
        if sp_param == None:
            body = {
              "aggs": {
                "2": {
                  "date_histogram": {
                    "field": "timestamp",
                    "fixed_interval": "30m",
                    "time_zone": "Asia/Shanghai",
                    "min_doc_count": 1
                  },
                  "aggs": {
                    "1": {
                      "sum": {
                        "field": "ti.score"
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
            } #全部
        else:
            body = {
              "aggs": {
                "2": {
                  "date_histogram": {
                    "field": "timestamp",
                    "fixed_interval": "30m",
                    "time_zone": "Asia/Shanghai",
                    "min_doc_count": 1
                  },
                  "aggs": {
                    "1": {
                      "sum": {
                        "field": "ti.score"
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
            } #按IP筛选
        try:
            ret = es.search(index='total', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            tims, number, jsontext = [], [], {}
            for i in re_data:
                time1 = i["key_as_string"].replace("T", " ")[11:-13]
                tims.append(time1)
                value = i["1"]["value"]
                number.append(round(value,2))

            jsontext['times'] = tims[:-1]
            jsontext['number'] = number[:-1]
            jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except Exception as err:
            logger.error('获取数据出错：{}'.format(err))
            return False

#WEB威胁安全趋势
class webthr(View):
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
                    match_phrase = {"match_phrase": {"dst_ip": ip}}
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
        st_time = request.POST['edtime']
        comid = request.POST['compid']
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')
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

    def sear_info(self,st_time,ed_time,sp_param):
        if sp_param == None:
            body = {
              "aggs": {
                "2": {
                  "date_histogram": {
                    "field": "timestamp",
                    "fixed_interval": "30m",
                    "time_zone": "Asia/Shanghai",
                    "min_doc_count": 1
                  },
                  "aggs": {
                    "1": {
                      "sum": {
                        "field": "waf.score"
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
            } #全部
        else:
            body = {
              "aggs": {
                "2": {
                  "date_histogram": {
                    "field": "timestamp",
                    "fixed_interval": "30m",
                    "time_zone": "Asia/Shanghai",
                    "min_doc_count": 1
                  },
                  "aggs": {
                    "1": {
                      "sum": {
                        "field": "waf.score"
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
            } #按IP筛选
        try:
            ret = es.search(index='total', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            tims, number, jsontext = [], [], {}
            for i in re_data:
                time1 = i["key_as_string"].replace("T", " ")[11:-13]
                tims.append(time1)
                value = i["1"]["value"]
                number.append(round(value,2))

            jsontext['times'] = tims[:-1]
            jsontext['number'] = number[:-1]
            jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except Exception as err:
            logger.error('获取数据出错：{}'.format(err))
            return False

#入侵检测威胁趋势
class inthr(View):
    @check_user_request
    def get(self,request):
        ed_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00')  # 东八区是按 秒和毫秒为整数
        st_time = (datetime.datetime.utcnow() + datetime.timedelta(days=-30)).strftime('%Y-%m-%dT%H:%M:00')
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
                    match_phrase = {"match_phrase": {"dst_ip": ip}}
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
                    "field": "timestamp",
                    "fixed_interval": "12h",
                    "time_zone": "Asia/Shanghai",
                    "min_doc_count": 1
                  },
                  "aggs": {
                    "1": {
                      "sum": {
                        "field": "snort.score"
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
            } #全部
        else:
            body = {
              "aggs": {
                "2": {
                  "date_histogram": {
                    "field": "timestamp",
                    "fixed_interval": "12h",
                    "time_zone": "Asia/Shanghai",
                    "min_doc_count": 1
                  },
                  "aggs": {
                    "1": {
                      "sum": {
                        "field": "snort.score"
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
            } #按IP筛选
        try:
            ret = es.search(index='total', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            tims, number, jsontext = [], [], {}
            for i in re_data:
                time1 = i["key_as_string"].replace("T", " ")[:-13]
                tims.append(time1)
                value = i["1"]["value"]
                number.append(round(value,2))

            jsontext['times'] = tims
            jsontext['number'] = number
            jsontext['edtime'] = ed_time
            return json.dumps(jsontext)
        except Exception as err:
            logger.error('获取数据出错：{}'.format(err))
            return False

#score_count 表格  威胁分类
class score_count(View):
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
                    match_phrase = {"match_phrase": {"dst_ip": ip}}
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
              "aggs": {
                "2": {
                  "terms": {
                    "field": "src_ip.keyword",
                    "order": {
                      "_count": "desc"
                    },
                    "size": 10
                  },
                  "aggs": {
                    "3": {
                      "terms": {
                        "field": "dst_ip.keyword",
                        "order": {
                          "_count": "desc"
                        },
                        "size": 10
                      },
                      "aggs": {
                        "4": {
                          "terms": {
                            "field": "snort.type.keyword",
                            "order": {
                              "_count": "desc"
                            },
                            "size": 10
                          },
                          "aggs": {
                            "5": {
                              "terms": {
                                "field": "ti.type.keyword",
                                "order": {
                                  "_count": "desc"
                                },
                                "size": 10
                              },
                              "aggs": {
                                "6": {
                                  "terms": {
                                    "field": "waf.type.keyword",
                                    "order": {
                                      "_count": "desc"
                                    },
                                    "size": 10
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
            } #全部
        else:
            body = {
              "aggs": {
                "2": {
                  "terms": {
                    "field": "src_ip.keyword",
                    "order": {
                      "_count": "desc"
                    },
                    "size": 10
                  },
                  "aggs": {
                    "3": {
                      "terms": {
                        "field": "dst_ip.keyword",
                        "order": {
                          "_count": "desc"
                        },
                        "size": 10
                      },
                      "aggs": {
                        "4": {
                          "terms": {
                            "field": "snort.type.keyword",
                            "order": {
                              "_count": "desc"
                            },
                            "size": 10
                          },
                          "aggs": {
                            "5": {
                              "terms": {
                                "field": "ti.type.keyword",
                                "order": {
                                  "_count": "desc"
                                },
                                "size": 10
                              },
                              "aggs": {
                                "6": {
                                  "terms": {
                                    "field": "waf.type.keyword",
                                    "order": {
                                      "_count": "desc"
                                    },
                                    "size": 10
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
            } #按IP筛选
        try:
            ret = es.search(index='total', doc_type='_doc', body=body)
            re_data = ret['aggregations']['2']['buckets']
            jsonlist = []
            for i in re_data:  #多个
                buck_a = i['3']['buckets']
                for v in buck_a:   #多个
                    try:
                        jsontext_1 = {}
                        #遍历数据
                        buck_b = v['4']['buckets']
                        y_id = v['key']    # 源IP
                        jsontext_1["y_id"] = y_id
                        number = v['doc_count']  #数量
                        jsontext_1["number"] = number
                        for k in buck_b:
                            m_ip = k['key']#目的IP
                            jsontext_1["m_ip"] = m_ip
                            buck_c = k['5']['buckets']
                            for c in buck_c:
                                w_ip = c['key']  # 威胁情报类型
                                jsontext_1["w_ip"] = w_ip
                                buck_d = c['6']['buckets']
                                for d in buck_d:
                                    waf_ip = d['key']  # waf类型
                                    jsontext_1["waf_ip"] = waf_ip
                        jsonlist.append(jsontext_1)
                    except Exception as err:
                        logger.error('威胁分类数据报错：{}'.format(err))
                    continue
            jstext = {}
            jstext['dat'] = jsonlist
            return jstext
        except Exception as err:
            logger.error('威胁情报-数据-获取数据出错：{}'.format(err))
            return False