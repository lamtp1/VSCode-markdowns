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

# cnx = mysql.connector.connect(user='root', password='123456',
#                               host='10.254.139.183', port=3306, database='CPM')
# cursor = cnx.cursor()

hafile = open("vm_cpu.txt", "w", encoding = 'UTF-8')
header_hafile="instance_name|instance|uuid|vCPU| \n"
hafile.write(header_hafile)

ha_qr= 'libvirt_cpu_stats_max_cpu{instance=~".*"}'
payload = {'query': ha_qr}
rq=requests.request("GET", url, headers=headers, auth=(usr, pas), params=payload).json()["data"]["result"]

for i in rq:
    if str(i["metric"]["monitor"]) != "openstack-hlct5":
        instance_name=i["metric"]["instance_name"]
        instance=i["metric"]["instance"]
        uuid=i["metric"]["uuid"]
        vCPU=i["value"][1]
        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        s=str(instance_name)  +"|" + str(instance) + "|" + str(uuid) + "|" + str(vCPU) + "|" + "\n"
        hafile.write(s)

        data =  {'instance_name': [instance_name],
                'instance': [instance],
                'uuid': [uuid],
                'vCPU': [vCPU],
                'insert_time': [insert_time]}                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO victoria_vm_cpu (instance_name, instance, uuid, vCPU, insert_time) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE  instance_name=%s, instance=%s, uuid=%s, vCPU=%s, insert_time=%s"
            val = (row['instance_name'], row['instance'], row['uuid'], row['vCPU'], insert_time, row['instance_name'], row['instance'], row['uuid'], row['vCPU'], insert_time)
#             cursor.execute(sql, val)

#         cnx.commit()

# cursor.close()
# cnx.close()
print('success')

