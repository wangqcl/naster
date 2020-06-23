import datetime
from pytz import timezone

'''东八区时间格式化'''
def time(utc_time,range):
    dict={"1":"%Y%m%d","2":"%Y%m%d-%H","3":"%Y%m%d-%H:%M","4":"%Y%m%d-%H:%M:%S"}
    if utc_time.find('Z') != -1:
        n_time = datetime.datetime.strptime(utc_time,'%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        n_time = datetime.datetime.strptime(utc_time,'%Y-%m-%dT%H:%M:%S.%f+08:00')
    utctime = datetime.datetime(n_time.year,n_time.month,n_time.day,n_time.hour,n_time.minute,n_time.second,tzinfo=timezone('UTC'))
    lt = utctime.astimezone(timezone('Asia/Shanghai'))
    llt = lt.strftime(dict.get("%s"% range))
    return llt