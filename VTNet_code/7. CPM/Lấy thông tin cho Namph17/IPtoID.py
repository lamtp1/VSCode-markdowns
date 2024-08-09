import requests
import json
import asyncore
from asyncio.windows_events import NULL # import NULL de lam gi?

url = 'http://dcim.viettel.vn/api/ipam/ip-addresses/'
service_url = 'http://dcim.viettel.vn/api/service/services/'

headers = {
    'Content-Type': "application/json",
    'Authorization': "Token   babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

ipfile = open("IP_namph17.txt", "r+", encoding='UTF-8')
w =  open('instances_id.txt', 'w', encoding='UTF-8')
w2 = open('ip_to_id.txt', 'w+', encoding='UTF-8')
for ip in ipfile:
    qr_ip = {"address":ip}
    try:
        rp= requests.request("GET", url, headers=headers, params=qr_ip).json()['results'][0]  # chuyen response ve json roi "di sau vao gia tri dau tien cua mang list result"?
    except IndexError:
        pass
    if rp['assigned_object'] !=None:
        if rp['assigned_object']['instance'] != None:
            as_name = str(rp['assigned_object']['instance']['id'])
            
    else:
        as_name= 'Null'  # bang None thi hien gi tren man hinh?

    # in instance id ra file text de lam dau vao lay service id
    s =  as_name + '\n'
    w2.write(s)

w2.close()
ipfile.close() 