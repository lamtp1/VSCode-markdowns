import requests
import json
import asyncore
from asyncio.windows_events import NULL
import pandas as pd
import openpyxl

service_url = 'http://10.255.58.203/api/service/service/'
manager_url = 'http://10.255.58.203/api/service/service-managers/'
owner_url = 'http://dcim.viettel.vn/api/service/service-owners/'
tenant_url = 'http://dcim.viettel.vn/api/user/employees/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp = requests.request("GET",service_url, headers=headers, params=temp_qr)
ip_count = rp.json()['count']

limit= 50
offset= 0
tenant_file = open("employee_tenant.txt", "w+", encoding='UTF-8')
while offset < 250 :
    querystring = {"limit":limit, "offset": offset}
    rp1 = requests.request("GET", service_url, headers=headers, params=querystring).json()['results']
    for id in rp1:
        service_id = str(id['id'])
        service_name = str(id['name'])
        qr_manager_owner = {"service_id": service_id}
        rp2 = requests.request("GET", manager_url, headers=headers, params=qr_manager_owner).json()['results'][0]
        service_manager = str(rp2['manager']['username'])
        rp3 = requests.request("GET", owner_url, headers=headers, params=qr_manager_owner).json()
        if rp3['count'] == 0:
            service_owner = 'Null'
        else:
            service_owner = str(rp3['results'][0]['owner']['username'])
        qr_tenant = {"username":service_owner}
        if qr_tenant == {"username": 'Null'}:
            owner_tenant = 'Null'
        else:
            rp4 = requests.request("GET", tenant_url, headers=headers, params=qr_tenant).json()
            if rp4['count'] != 1:
                owner_tenant = 'Null'
            else:
                owner_tenant = str(rp4['results'][0]['tenant']['name'])

        s =  service_id + '|' + service_name + '|' + service_manager + '|' + service_owner + '|' +owner_tenant + '|'  +'\n'
        print(s)
        tenant_file.write(s)

    offset = offset + 50  
tenant_file.close()
