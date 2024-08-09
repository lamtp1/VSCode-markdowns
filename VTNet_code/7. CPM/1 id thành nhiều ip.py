import requests
import json
import asyncore
from asyncio.windows_events import NULL 

url = 'http://dcim.viettel.vn/api/dcim/instance-interfaces/'
ipam_url = 'http://dcim.viettel.vn/api/ipam/ip-addresses/'

headers = {
    'Content-Type': "application/json",
    'Authorization': "Token  babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

instance_file =  open('INSTANCE.txt', 'r', encoding='UTF-8')
# w = open('interface_id.txt', 'w', encoding='UTF-8')
w2 = open('instance_to_ip.txt', 'w+', encoding='UTF-8')
for instance_id in instance_file:
    qr_id = {"instance_id":instance_id.strip()}
    try:
        rp= requests.request("GET", url, headers=headers, params=qr_id).json()['results']
    except Exception:
        pass
    for id in rp:       # tat ca cac interface trong response
        interface_id = str(id['id'])
        instance_name = str(id['instance']['name'])
        qr_id2 = {"interface_id":interface_id}
        if id['count_ipaddresses'] == 1:
            rp2 = requests.request("GET", ipam_url, headers=headers, params=qr_id2).json()['results'][0]
            ip_1 = rp2['address']
            ip_2 = ip_1.split('/')[0]
        else:
            ip = 'không có ip'

        # print(instance_id.strip() + '|' + interface_id + '|'+ ip.strip() )
        s2 = instance_id.strip() +  '|' + instance_name + '|' + ip_2.strip() + '\n'
        w2.write(s2)
# w.close()
w2.close()                   # dung o w.close thi co tat ca interface_id và ip
instance_file.close() 

 
            
    