from asyncio.windows_events import NULL
import asyncore
from re import I, S, search
import requests
import json
import datetime
import time
import calendar
import re

url = "http://10.254.139.73:8501/api/v1/query"
usr="npms"
pas="Npms@123"

headers = {
    'Content-Type': "application/json",
    'Content-Encoding': "gzip",
    'Cache-Control': "no-cache",
    }
hafile = open("test.txt", "w")
header_hafile="Volume type|Used|HA Name|Cloud cluster|check IP \n"
hafile.write(header_hafile)
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
    if len(get_ha) > 0:
        s=str(vl_type_name) + "|"+ str(get_vl_used) + "|" + str(get_ha) + "|" + str(get_cloudname) + "|" + str(checkIP) + "\n"
        hafile.write(s)
    else:
        s=str(vl_type_name)  +"|" + str(get_vl_used) + "|" + "Not in HA" + "|" +"Not in Cloud" + "|" + str(checkIP) + "\n"
        hafile.write(s)
hafile.close()
