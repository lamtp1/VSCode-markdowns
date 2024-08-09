import requests
import json
import asyncore
from asyncio.windows_events import NULL

service_url = 'http://dcim.viettel.vn/api/service/service/'
ip_url = 'http://dcim.viettel.vn/api/service/service-users/'
instance_url = 'http://dcim.viettel.vn/api/dcim/instances/'

headers = {
    'Content-Type': "application/json",
    'Authorization': "Token     babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

service_ids = open("lamtp1.txt", "r")
w =  open('service_to_ip_converter.txt', 'w', encoding='UTF-8')
for service_id in service_ids:
    qr_param1 = {"service_id":service_id}
    rp1 = requests.request("GET", ip_url , headers=headers, params=qr_param1).json()
    count = str(rp1['count'])
    offset = 0
    limit = count
    while offset < count:
        qr_param = {"service_id":service_id, "limit":limit, "offset": offset}
        rp2 = requests.request("GET", ip_url , headers=headers, params=qr_param).json()['results']
      
        for id in rp2:
            service_id = str(['service']['id'])
            service_code = str(id['service']['code'])
            service_name = str(id['service']['name'])
            instance_id = str(id['instance']['id'])

            rp3 = requests.request("GET", instance_url+instance_id , headers=headers).json()
            ip = str(rp3['primary_ip4']['address'])
            s =  service_id + '|' + service_code + '|' +  service_name + '|' + instance_id + '|' + ip + '\n'
            w.write(s)
        offset = offset + count
   

w.close()
service_ids.close()
