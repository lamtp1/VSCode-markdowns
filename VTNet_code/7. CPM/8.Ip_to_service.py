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

ipfile = open("cpm_ip.txt", "r")
w =  open('instances_id.txt', 'w', encoding='UTF-8')
w2 = open('ip_to_service.txt', 'w', encoding='UTF-8')
for ip in ipfile:
    qr_ip = {"address":ip}
    rp= requests.request("GET", url, headers=headers, params=qr_ip).json()['results'][0]  # chuyen response ve json roi "di sau vao gia tri dau tien cua mang list result"?
    if rp['assigned_object'] !=None:
        if rp['assigned_object']['instance'] != None:
            as_name = rp['assigned_object']['instance']['id']
            
    else:
        as_name= None  # bang None thi hien gi tren man hinh?

    # in instance id ra file text de lam dau vao lay service id
    w.write(str(as_name)+"\n")

    if as_name != None:
        instance_id = {"instance_id":as_name}
        rp2 = requests.request("GET", service_url , headers=headers, params=instance_id).json()['results']
        for id in rp2:
            i=rp2.index(id) # moi id trong response se duoc danh index bat dau tu 0
            rp2i = rp2[i]
            service = str(rp2i['name'])
            print (ip.strip() + ' ' + service)
            s = ip.strip() + ' ' + service + '\n'
            w2.write(s)
    else:
        service = None
 
w.close()
w2.close()
ipfile.close() 

# instance_file = open("instances_id.txt", "r")
# for instance_id in instance_file:
#     instance_id = {"instance_id":as_name}
#     rp2 = requests.request("GET", service_url, headers=headers, params=instance_id).json()['results'][1]  # chuyen response ve json roi "di sau vao gia tri dau tien cua mang list result"?
#     if rp2['code'] !=None:
#         service_code = rp2['code'] 
    # else:
    #     service_code = None

    # print (service_code)      
            
    