import requests
import json
import asyncore
from asyncio.windows_events import NULL

service_url = 'http://dcim.viettel.vn/api/service/service/'
ip_url = 'http://dcim.viettel.vn/api/service/service-users/'

headers = {
    'Content-Type': "application/json",
    'Authorization': "Token   babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

service_file = open("service_code.txt", "r")
w =  open('service_to_ip.txt', 'w', encoding='UTF-8')

for code in service_file:
    qr_code = {"code":code}
    rp= requests.request("GET", service_url, headers=headers, params=qr_code).json()['results'][0]
    if rp['id'] !=None:
        service_id = rp['id']
    else:
        service_id = None

    if service_id != None:
        service_id = {"service_id":service_id}
        rp2 = requests.request("GET", ip_url , headers=headers, params=service_id).json()['results'][0] # sao phai de results 0 moi chay dc
        ip = str(rp2['instance']['display'])
    else:
        service = None

    print ('Ma dich vu: ' + code.strip() + ' ' + 'co IP la: '+ ip + '\n')
    s = 'Ma dich vu: ' + code.strip() + ' ' + 'co IP la: '+ ip + '\n'
    w.write(s)
w.close()
service_file.close()