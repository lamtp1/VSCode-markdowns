import requests
import json
import asyncore
from asyncio.windows_events import NULL 

url = 'http://dcim.viettel.vn/api/dcim/instance-interfaces/'
ipam_url = 'http://dcim.viettel.vn/api/ipam/ip-addresses/'

headers = {
    'Content-Type': "application/json",
    'Authorization': "Token  b1e04e3e48706fa80132baa3753336de382a9f25",
    'Cache-Control': "no-cache",
    }

instance_file =  open('instances_id.txt', 'r', encoding='UTF-8')
# w = open('interface_id.txt', 'w', encoding='UTF-8')
w2 = open('interface_to_ip.txt', 'w', encoding='UTF-8')
for instance_id in instance_file:
    qr_id = {"instance_id":instance_id.strip()}
    rp= requests.request("GET", url, headers=headers, params=qr_id).json()['results']
    for id in rp:       # tat ca cac interface trong response
        interface_id = str(id['id'])
        qr_id2 = {"interface_id":interface_id}
        if id['count_ipaddresses'] == 1:
            rp2 = requests.request("GET", ipam_url, headers=headers, params=qr_id2).json()['results'][0]
            ip = rp2['address']
        else:
            ip = 'không có ip'

        print(instance_id.strip() + ' ' + interface_id + ' '+ ip.strip() )
        s2 = instance_id.strip() + ' ' + interface_id + ' '+ ip.strip() + '\n'
        w2.write(s2)
# w.close()
w2.close()                   # dung o w.close thi co tat ca interface_id và ip
instance_file.close() 

 
            
    