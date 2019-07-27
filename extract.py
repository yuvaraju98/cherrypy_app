import requests, zipfile, io
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import csv
import os
import redis

def load_redis():
    redis_host = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
    # redis_host= 'redis://localhost:6379'
    r = redis.StrictRedis.from_url(redis_host,  decode_responses=True)
    # r = redis.Redis()

    zp='https://www.bseindia.com/download/BhavCopy/Equity/EQ250719_CSV.ZIP'
    req = requests.get(zp)
    z = zipfile.ZipFile(io.BytesIO(req.content))
    z.extractall()
    line=pd.read_csv('EQ250719.CSV')
    import json
    keys=list()
    for x,y in line.T.iteritems():
        r.hmset('hashName',  {'code':y['SC_CODE'],'open':y['OPEN'],'high':y['HIGH'],'low':y['LOW'],'close':y['CLOSE']})
        r.hmset(y['SC_NAME'].strip(),r.hgetall('hashName'))
        # print(y['SC_CODE'])
        r.lpush('keys',y['SC_NAME'].strip())
load_redis()
