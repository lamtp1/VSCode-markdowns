import requests
import json
import asyncore
from asyncio.windows_events import NULL

service_url = 'http://dcim.viettel.vn/api/service/service/'
ip_url = 'http://dcim.viettel.vn/api/service/service-users/'
instance_url = 'http://dcim.viettel.vn/api/dcim/instances/'

headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    7e4ed69be74cfd475a1c361002b15b0169420f08",
    'Cache-Control': "no-cache",
    }

service_file = open("service_code.txt", "r")
w =  open('Chuyen_service_instance.txt', 'w', encoding='UTF-8')
for code in service_file:
    qr_code = {"code":code}
    rp= requests.request("GET", service_url, headers=headers, params=qr_code).json()['results'][0]
    if rp['id'] !=None:
        service_id = str(rp['id'])
        service_code = str(rp['code'])
        service_name = str(rp['name'])
    else:
        service_id = None  # co hien thi gi tren man hinh khong?

    if service_id != None:
        count = requests.request("GET", ip_url , headers=headers, params=service_id).json()['count']
        offset = 0
        limit = count
        while offset < count:
            qr_param = {"service_id":service_id, "limit":limit, "offset": offset}
            rp2 = requests.request("GET", ip_url , headers=headers, params=qr_param).json()['results']
            for id in rp2:
                instance_id = str(id['instance']['id'])
                rp3 = requests.request("GET", instance_url+instance_id , headers=headers).json()
                if rp3['primary_ip4'] != None:
                    ip = str(rp3['primary_ip4']['address'])
                else:
                    ip = 'None'
                # print ( code.strip() + ' ' +  ip + '\n')
                s =  service_id + '|' + service_code + '|' + service_name + '|' + instance_id + "|" + ip + '\n'
                # print(s)
                w.write(s)
            offset = offset + count
    else:
        service = None

w.close()
service_file.close()
