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
# hafile = open("test2.txt", "w")
# header_hafile="Volume type|Used|HA Name|Cloud cluster|check IP \n"
# hafile.write(header_hafile)
vl_type_qr={'query':'count by(type) (cinder_volumes{monitor!="openstack-hlct5"})'}
get_vl_type=requests.request("GET", url, headers=headers, auth=(usr, pas), params=vl_type_qr).json()["data"]["result"]
for i in get_vl_type:
    vl_type_name= i["metric"]["type"]
    c=vl_type_name.split('_')
    d=[i for i in c]
    checkIP=''
    for j in d:
     if len(j)>=8:
        if j.find("10")!=-1:
            checkIP=j
    vm_qr={'query':'cinder_volumes{status="in-use",type="'+ str(vl_type_name)+'"}'}
    vm_tmp=requests.request("GET", url, headers=headers, auth=(usr, pas), params=vm_qr).json()["data"]["result"]
    vl_used_qr={'query':'sum by(type)(cinder_volumes{type="'+str(vl_type_name)+'"})'}
    get_vl_used=requests.request("GET", url, headers=headers, auth=(usr, pas), params=vl_used_qr).json()["data"]["result"][0]["value"][1]
    get_compute_ip=''
    get_ha=''
    insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for j in vm_tmp:
        vm_uuid=j["metric"]["server_id"]
        compute_qr={'query':'libvirt_cpu_stats_cpu_time_seconds{uuid="'+ str(vm_uuid)+'"}'}
        get_compute_ip_tmp=requests.request("GET", url, headers=headers, auth=(usr, pas), params=compute_qr).json()["data"]["result"]
        if len(get_compute_ip_tmp) > 0:
            get_compute_ip=get_compute_ip_tmp[0]["metric"]["instance"]
            break
    if len(get_compute_ip)>0:
        compute_ip=get_compute_ip.split(':',1)[0]
        compute_name_qr={'query':'topk(1, node_uname_info{instance=~"'+str(compute_ip)+':.*"})'}
        get_compute_name=requests.request("GET", url, headers=headers, auth=(usr, pas), params=compute_name_qr).json()["data"]["result"][0]["metric"]["nodename"]
        ha_qr={'query':'hypervisor_memory_mbs_total{hypervisor_hostname="'+str(get_compute_name)+'"}'}
        get_ha=requests.request("GET", url, headers=headers, auth=(usr, pas), params=ha_qr).json()["data"]["result"][0]["metric"]["aggregate"]
        get_cloudname=requests.request("GET", url, headers=headers, auth=(usr, pas), params=ha_qr).json()["data"]["result"][0]["metric"]["monitor"]
    if len(get_ha) == 0:
        # s=str(vl_type_name) + "|"+ str(get_vl_used) + "|" + str(get_ha) + "|" + str(get_cloudname) + "|" + str(checkIP) + "\n"
        # hafile.write(s)
        get_ha = "Not in HA"
        get_cloudname = "Not in Cloud"
    s=str(vl_type_name)  +"|" + str(get_vl_used) + "|" + get_ha + "|" + get_cloudname + "|" + str(checkIP) + "\n"
    # hafile.write(s)

    data =  {'volume_type': [vl_type_name],
            'used': [get_vl_used],
            'ha_name': [get_ha],
            'cloud_cluster': [get_cloudname],
            'check_ip': [checkIP],
            'insert_time': [insert_time]}                
    df = pd.DataFrame(data)           
    for index, row in df.iterrows():
        sql = "INSERT INTO victoria_cloud_ha_used (volume_type, used, ha_name, cloud_cluster, check_ip, insert_time) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE  volume_type=%s, used=%s, ha_name=%s, cloud_cluster=%s, check_ip=%s, insert_time=%s"
        val = (row['volume_type'], row['used'], row['ha_name'], row['cloud_cluster'], row['check_ip'], insert_time, row['volume_type'], row['used'], row['ha_name'], row['cloud_cluster'], row['check_ip'], insert_time)
        cursor.execute(sql, val)

    cnx.commit()

cursor.close()
cnx.close()
print('success')

# hafile.close()
