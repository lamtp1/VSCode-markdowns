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

ha_qr= 'hypervisor_memory_mbs_used{aggregate=~".*"}/1024'
payload = {'query': ha_qr}
rq=requests.request("GET", url, headers=headers, auth=(usr, pas), params=payload).json()["data"]["result"]
for i in rq:
    if str(i["metric"]["monitor"]) != "openstack-hlct5":
        Hostname_compute=i["metric"]["hypervisor_hostname"]
        ha_name = i["metric"]["aggregate"]
        IP_Compute=i["metric"]["instance"].split(':',1)[0]
        Cum_Cloud=i["metric"]["monitor"]
        RAM=i["value"][1]
        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data =  {'Hostname_compute': [Hostname_compute],
                'ha_name': [ha_name],
                'IP_Compute': [IP_Compute],
                'Cum_Cloud': [Cum_Cloud],
                'RAM': [RAM],
                'insert_time': [insert_time]}                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO victoria_compute_used_ram (Hostname_compute, ha_name, IP_Compute, Cum_Cloud, RAM, insert_time) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE  Hostname_compute=%s, IP_Compute=%s, Cum_Cloud=%s, RAM=%s, insert_time=%s"
            val = (row['Hostname_compute'], row['ha_name'], row['IP_Compute'], row['Cum_Cloud'], row['RAM'], insert_time, row['Hostname_compute'], row['IP_Compute'], row['Cum_Cloud'], row['RAM'], insert_time)
            cursor.execute(sql, val)

        cnx.commit()

cursor.close()
cnx.close()
print('success')

