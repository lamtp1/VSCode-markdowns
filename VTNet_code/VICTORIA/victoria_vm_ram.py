import asyncore
from operator import is_not
from queue import Empty
from re import I, S, search
import requests
import json
from datetime import datetime
import time
import calendar
import re
import pandas as pd
import mysql.connector

url = "http://10.254.139.73:8501/api/v1/query"
usr="npms"
pas="Npms@123"

headers = {
    'Content-Type': "application/json",
    'Content-Encoding': "gzip",
    'Cache-Control': "no-cache",
    }

cnx = mysql.connector.connect(user='root', password='123456',
                              host='10.254.139.183', port=3306, database='CPM')
cursor = cnx.cursor()


ha_qr= 'libvirt_mem_stats_actual{ instance=~".*"}/1024/1024'
payload = {'query': ha_qr}
rq=requests.request("GET", url, headers=headers, auth=(usr, pas), params=payload).json()["data"]["result"]

for i in rq:
    if str(i["metric"]["monitor"]) != "openstack-hlct5":
        instance_name=i["metric"]["instance_name"]
        instance=i["metric"]["instance"]
        uuid=i["metric"]["uuid"]
        RAM=i["value"][1]
        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data =  {'instance_name': [instance_name],
                'instance': [instance],
                'uuid': [uuid],
                'RAM': [RAM],
                'insert_time': [insert_time]}                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO victoria_vm_ram (instance_name, instance, uuid, RAM, insert_time) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE  instance_name=%s, instance=%s, uuid=%s, RAM=%s, insert_time=%s"
            val = (row['instance_name'], row['instance'], row['uuid'], row['RAM'], insert_time, row['instance_name'], row['instance'], row['uuid'], row['RAM'], insert_time)
            cursor.execute(sql, val)

        cnx.commit()

cursor.close()
cnx.close()
print('success')

