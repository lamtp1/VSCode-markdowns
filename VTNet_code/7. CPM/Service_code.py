import requests
import json
import asyncore
from asyncio.windows_events import NULL


service_url = 'http://10.255.58.203/api/service/services/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",service_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

limit= 250
offset= 0
service_file = open("service_id.txt", "w+", encoding = 'UTF-8')
while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", service_url , headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name
        service_id = str(id['id'])

        s =  service_id +"\n"
        service_file.write(s)
    offset = offset + 250                                 

service_file.close()