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

# ouputfile = open("Cloud_ha.txt", "w", encoding="utf-8")
ha_qr= 'hypervisor_memory_mbs_total'
payload = {'query': ha_qr}
rq=requests.request("GET", url, headers=headers, auth=(usr, pas), params=payload).json()["data"]["result"]
cmt="Cloud cluster|HA Name|Compute hostaname|Compute Ip|Compute status\n"
# ouputfile.write(cmt)
for i in rq:
    if str(i["metric"]["monitor"]) != "openstack-hlct5":
        cloud_cluster=str(i["metric"]["monitor"])
        ha_name=str(i["metric"]["aggregate"])
        compute_hm=str(i["metric"]["hypervisor_hostname"])
        nova_status=str(i["metric"]["nova_service_status"])

        cp_ip='node_uname_info{monitor=~"' + str(cloud_cluster) + '",nodename=~"' + str(compute_hm) + '"}'
        payload_02={'query': cp_ip}
        rq_ip=requests.request("GET", url, headers=headers, auth=(usr, pas), params=payload_02).json()["data"]["result"]
        if len(rq_ip) > 0:
            compute_ip=str(rq_ip[0]["metric"]["instance"].split(':',1)[0])

        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        data =  {'cloud_cluster': [cloud_cluster],
                'ha_name': [ha_name],
                'compute_hm': [compute_hm],
                'compute_ip': [compute_ip],
                'nova_status': [nova_status],
                'insert_time': [insert_time]}                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO Cloud_HA (cloud_cluster, ha_name, compute_hm, compute_ip, nova_status, insert_time) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE  cloud_cluster=%s, ha_name=%s, compute_hm=%s, compute_ip=%s, nova_status=%s"
            val = (row['cloud_cluster'], row['ha_name'], row['compute_hm'], row['compute_ip'], row['nova_status'], insert_time, row['cloud_cluster'], row['ha_name'], row['compute_hm'], row['compute_ip'], row['nova_status'])
            cursor.execute(sql, val)

        cnx.commit()

cursor.close()
cnx.close()
print('success')
            # s= str(cloud_cluster) + "|" + str(ha_name) + "|" + str(compute_hm) + "|" + str(compute_ip) + "|" +  str(nova_status) + "\n"
            # ouputfile.write(s)
# ouputfile.close()

