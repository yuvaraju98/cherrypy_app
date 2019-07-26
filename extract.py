import requests, zipfile, io
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import csv
import redis


zp='https://www.bseindia.com/download/BhavCopy/Equity/EQ250719_CSV.ZIP'
r = requests.get(zp)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()
line=pd.read_csv('EQ250719.CSV')
r = redis.Redis()
import json
keys=list()
for x,y in line.T.iteritems():
    r.hmset('hashName',  {'name':y['SC_NAME'],'open':y['OPEN'],'high':y['HIGH'],'low':y['LOW'],'close':y['CLOSE']})
    r.hmset(y['SC_CODE'],r.hgetall('hashName'))
    print(y['SC_CODE'])
    r.lpush('keys',y['SC_CODE'])
