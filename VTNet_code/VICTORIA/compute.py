# from asyncio
import asyncore
from operator import is_not
from queue import Empty
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
ouputfile = open("test_compute.txt", "w", encoding="utf-8")
ha_qr= 'hypervisor_vcpus_total{aggregate=~".*"}'
payload = {'query': ha_qr}
rq=requests.request("GET", url, headers=headers, auth=(usr, pas), params=payload).json()["data"]["result"]
cmt="Cloud cluster|HA Name|Compute hostaname|Compute Ip|Compute status\n"
ouputfile.write(cmt)
for i in rq:
    if str(i["metric"]["monitor"]) != "openstack-hlct5":
        cloud_cluster=i["metric"]["monitor"]
        ha_name=i["metric"]["aggregate"]
        compute_hm=i["metric"]["hypervisor_hostname"]
        nova_status=i["metric"]["nova_service_status"]
        value=i["value"][1]
#        cp_ip='node_uname_info{monitor=~"' + str(cloud_cluster) + '",nodename=~"' + str(compute_hm) + '"}'
#        payload_02={'query': cp_ip}
#        rq_ip=requests.request("GET", url, headers=headers, auth=(usr, pas), params=payload_02).json()["data"]["result"]
        # if len(rq_ip) > 0:
        #     compute_ip=rq_ip[0]["metric"]["instance"].split(':',1)[0]
        s= str(cloud_cluster) + "|" + str(ha_name) + "|" + str(compute_hm) + "|" + str(nova_status) + "|" +  str(nova_status) + str(value)+"\n"
        ouputfile.write(s)
            # print(s)
ouputfile.close()

