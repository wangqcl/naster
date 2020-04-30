from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from elasticsearch import Elasticsearch
import json

# Create your views here.
def index(request):
    '''前台首页'''
    #return HttpResponse("欢迎进入前台首页！")
    return render(request,"web/index.html")

def test(request):
    # 连接es时host只写ip
    es_host = 'http://172.16.20.60'
    #es = Elasticsearch(hosts=es_host, port=9200, timeout=15000)
    es = Elasticsearch(
        ['172.16.20.60', '9200'],
        http_auth=('elastic', 'hqsec711'),
        scheme="http",
        port=9200,
    )

    body = {
        "_source": ["source.bytes"],   # 指定 _source下的字段名字  可以.字段
        "query": {
            "bool": {
                "must": [{
                    "range": {  # range查询区间范围
                        "source.bytes": {
                            "gt": "301",
                            "lt": "305"
                        }
                    }
                }],
                "must_not": [],
                "should": []
            }
        },
        "from": 0,  # 返回的数据量范围，
        "size": 10,
        "sort": [],
        "aggs": {}
    }
    list = []
    ret = es.search(index='packetbeat-7.4.0-2020.03.26-000001', doc_type='_doc',body=body)
    #print(ret['hits']['hits'])  #[0]['_source']['source']
    re_data = ret['hits']['hits']
    print(len(re_data))
    for i in re_data:
        #print(i['_source']['source']['bytes'])
        x = i['_source']['source']['bytes']
        list.append(x)
    print(list)
    myset = set(list)  #去重

    #定义一个变量
    jsontext = {}

    for item in myset:
        print("the %d has found %d" % (item, list.count(item)))
        jsontext[item] = list.count(item)

    return HttpResponse(json.dumps(jsontext))
    # res = {
    #     "a": 11100,
    #     "b": 200,
    #     "c": 300,
    #     "d": 400,
    #     "e": 900,
    #     "f": 400,
    # }

    #return JsonResponse(res)
    #return HttpResponse(json.dumps(res))