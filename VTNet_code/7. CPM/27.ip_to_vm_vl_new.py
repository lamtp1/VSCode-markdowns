import requests
import json
import asyncore
from asyncio.windows_events import NULL # import NULL de lam gi?
import pandas as pd
import openpyxl
import requests

ip_url = 'http://dcim.viettel.vn/api/ipam/ip-addresses/'
instance_url = 'http://dcim.viettel.vn/api/dcim/instances/'

headers = {
    'Content-Type': "application/json",
    'Authorization': "Token   babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

ipfile = open("cpm_ip.txt", "r", encoding='UTF-8')

for ip in ipfile:
    qr_ip = {"address":ip}
    rp= requests.request("GET", ip_url, headers=headers, params=qr_ip).json()['results'][0]
    instance_id = str(rp['assigned_object']['instance']['id'])
    # print(instance_id + "\n")
    rp2 = requests.request("GET", instance_url + instance_id, headers=headers).json()
    if rp2['parent_instance'] == None:
        loai = 'VL'
        parent_instance = 'Nothing'
        status = str(rp2['status']['label'])        
    else:
        loai = 'VM'
        parent_instance_id = str(rp2['parent_instance']['id'])
        rp3 = requests.request("GET", instance_url+parent_instance_id, headers=headers).json()
        if rp3['primary_ip4'] != None:
            parent_instance = str(rp3['primary_ip4']['address'])
        else:
            parent_instance = str(rp3['name'])
        status = str(rp2['status']['label'])      
    if rp2['cloud_instance_uuid'] != None:
        Cloud_instance_uuid = str(rp2['cloud_instance_uuid'])
    else:
        Cloud_instance_uuid = "Nothing"
    data =  {'Server': [ip],
            'Type': [loai],
            'Status': [status],
            'Cloud_instance_uuid': [Cloud_instance_uuid],
            'Parent_instance': [parent_instance]}
                
    df = pd.DataFrame(data)
    try:
            existing_df = pd.read_excel("Server_info_new_3.xlsx")
            df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_excel("Server_info_new_3.xlsx", index=False)

ipfile.close() 

  
