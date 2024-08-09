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

# ouputfile = open("compute_total_cpu_ratio.txt", "w", encoding="utf-8")

ha_qr= 'hypervisor_vcpus_total{aggregate=~".*"}'
ha_qr_2 = 'openstack_allocation_ratio{cloud=~".*",resource="vcpu"}'
payload = {'query': ha_qr}
payload_2 = {'query': ha_qr_2}
rq=requests.request("GET", url, headers=headers, auth=(usr, pas), params=payload).json()["data"]["result"]
rq2=requests.request("GET", url, headers=headers, auth=(usr, pas), params=payload_2).json()["data"]["result"][0]
ratio = int(rq2["value"][1])

for i in rq:
    if str(i["metric"]["monitor"]) != "openstack-hlct5":
        Hostname_compute=i["metric"]["hypervisor_hostname"]
        ha_name = i["metric"]["aggregate"]
        IP_Compute=i["metric"]["instance"].split(':',1)[0]
        Cum_Cloud=i["metric"]["monitor"]
        vCPU=int(i["value"][1])
        vCPU_ratio = ratio*vCPU
        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # s= str(Hostname_compute) + "|" + str(ha_name) + "|" + str(vCPU) + "|" + str(ratio) + "|" +  str(vCPU_ratio) +"\n"

        # ouputfile.write(s)
            # print(s)

        data =  {'Hostname_compute': [Hostname_compute],
                'ha_name': [ha_name],
                'IP_Compute': [IP_Compute],
                'Cum_Cloud': [Cum_Cloud],
                'vCPU': [vCPU],
                'ratio': [ratio],
                'vCPU_ratio': [vCPU_ratio],
                'insert_time': [insert_time]}                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO victoria_compute_total_cpu (Hostname_compute, ha_name, IP_Compute, Cum_Cloud, vCPU, ratio, vCPU_ratio, insert_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE  Hostname_compute=%s, IP_Compute=%s, Cum_Cloud=%s, vCPU=%s, insert_time=%s"
            val = (row['Hostname_compute'], row['ha_name'], row['IP_Compute'], row['Cum_Cloud'], row['vCPU'], row['ratio'], row['vCPU_ratio'], insert_time, row['Hostname_compute'], row['IP_Compute'], row['Cum_Cloud'], row['vCPU'], insert_time)
            cursor.execute(sql, val)

        cnx.commit()

cursor.close()
cnx.close()
print('success')
# ouputfile.close()

