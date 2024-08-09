import asyncore
import json
from asyncio.windows_events import NULL
from re import S
import pandas as pd
import openpyxl
import requests

# lay ipv4 primary tu api instance
instance_url = 'http://dcim.viettel.vn/api/dcim/instances/'
site_url = 'http://dcim.viettel.vn/api/dcim/devices/'
owner_url = 'http://dcim.viettel.vn/api/service/service-owners/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

instance_id_file = open("instance_id_file_2.txt", "r", encoding='UTF-8')
device_file = open("device_namph17_2.txt", "w+", encoding='UTF-8')
for instance_id in instance_id_file: 
    rp2= requests.request("GET",instance_url+instance_id, headers=headers).json()
    if rp2['primary_ip4'] != None:
        instance_id = str(rp2['id'])
        primary_ip = str(rp2['primary_ip4']['display'])      # dung tai primary_ip thi chi co 1 ip
        owner = str(rp2["manager"]["username"])
        if rp2['tenant'] != None:
            tenant = str(rp2['tenant']['name'])
        else:
            tenant = None
        if rp2['parent_instance'] == None:      # check ao hoa lan 1
            loai = 'Vật lý'
            device_id = str(rp2['device']['id'])
            rp3 = requests.request("GET",site_url+device_id, headers=headers, timeout=30).json()
            site = str(rp3['site']['name'])
            location = str(rp3['location']['name'])
            device_type = str(rp3['device_type']['display'])
        else:
            loai = 'CLOUD'    
            parent_id = str(rp2['parent_instance']['id'])
            rp = requests.request("GET",instance_url+parent_id, headers=headers).json()  # can luu y
            if rp['parent_instance'] != None:  # check ao hoa lan 2
                parent_id = str(rp['parent_instance']['id'])
                rp = requests.request("GET",instance_url+parent_id, headers=headers).json()
                if rp['parent_instance'] != None:  # check ao hoa lan 3
                    parent_id = str(rp['parent_instance']['id'])
                    rp = requests.request("GET",instance_url+parent_id, headers=headers).json()
                    device_id = str(rp['device']['id'])
                    rp3 = requests.request("GET",site_url+device_id, headers=headers).json()
                    site = str(rp3['site']['name'])
                    location = str(rp3['location']['name'])
                    device_type = str(rp3['device_type']['display'])
                else:
                    device_id = str(rp['device']['id'])
                    rp3 = requests.request("GET",site_url+device_id, headers=headers).json()
                    site = str(rp3['site']['name'])
                    try:
                        location = str(rp3['location']['name'])
                    except KeyError:
                        pass
                    device_type = str(rp3['device_type']['display'])
            else:
                device_id = str(rp['device']['id'])
                rp3 = requests.request("GET",site_url+device_id, headers=headers).json()
                site = str(rp3['site']['name'])
                try:
                    location = str(rp3['location'])
                except KeyError:
                    pass
                device_type = str(rp3['device_type']['display'])
    
        if tenant == None:
            s =  instance_id + '|' + primary_ip + '|' + loai + '|' + site + '|' + location + '|' + device_type + "|" + owner + '\n'
        else:
            s =  instance_id + '|' + primary_ip + '|' + loai + '|' + site + '|'+ location + '|' + device_type + "|" + tenant + '|' + owner +'\n'

        device_file.write(s)
                                           
device_file.close()

