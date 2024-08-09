import asyncore
import json
from asyncio.windows_events import NULL
from re import S

import requests

# lay ipv4 primary tu api instance
instance_url = 'http://dcim.viettel.vn/api/dcim/instances/'
site_url = 'http://dcim.viettel.vn/api/dcim/devices/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }
rp1 = requests.request("GET",instance_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

limit= 250
offset= 0
instance_file = open("instance_info_new.txt", "w+", encoding='UTF-8')
while offset < ip_count :
    querystring = {"limit":limit, "offset": offset}
    rp2= requests.request("GET",instance_url, headers=headers, params=querystring).json()['results']
    for id in rp2:
        if id['primary_ip4'] != None:
            instance_id = str(id['id'])
            primary_ip = str(id['primary_ip4']['display'])      # dung tai primary_ip thi chi co 1 ip
            if id['parent_instance'] == None:
                loai = 'Vật lý'
                device_id = str(id['device']['id'])
                qr_param = {"id": device_id}
                rp3 = requests.request("GET",site_url, headers=headers, params=qr_param).json()['results'][0]
                site = str(rp3['site']['name'])
            else:
                loai = 'Ảo hóa'
                device_id = None
            if device_id != None:
                s =  instance_id + ' '+ primary_ip + ' ' + loai + ' ' + site + '\n'
            else:
                s =  instance_id + ' '+ primary_ip + ' ' + loai + '\n'
            # print(s)
            instance_file.write(s)                         # het vong for se co 3 ip
        else:
            primary_ip = None
    offset = offset + 250                                            # de offset ngoai vong for se bi lap 3 lan => de offset ben trong
instance_file.close()
