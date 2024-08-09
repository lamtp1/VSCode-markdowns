import asyncore
import json
from asyncio.windows_events import NULL
from re import S
import pandas as pd
import openpyxl
import requests

# lay ipv4 primary tu api instance
device_url = 'http://dcim.viettel.vn/api/dcim/devices/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }
rp1 = requests.request("GET",device_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

limit= 50
offset= 0
while offset <  250:
    querystring = {"limit":limit, "offset": offset}
    rp2= requests.request("GET", device_url, headers=headers, params=querystring).json()['results']
    for id in rp2:
        device_id = str(id['id'])
        device_name = str(id['name'])
        device_type = str(id['device_type']['display'])
        device_type_manufacture = str(id['device_type']['manufacturer']['display'])
        device_role = str(id['device_role']['display'])
        serial = str(id['serial'])
        site = str(id['site']['name'])
        if id['location'] != None:
            location = str(id['location']['display'])
        else:
            location = 'null'
        if id['rack'] != None:
            rack = str(id['rack']['display'])
        else:
            rack = 'null'
        status = str(id['status']['label'])
        if id['primary_ip4'] != None:
            primary_ip4 = str(id['primary_ip4']['address'])
        else:
            primary_ip4 = 'null'
        manager_name = str(id['manager']['username'])
        manager_mail = str(id['manager']['email'])
        if id['switch'] != None:
            switch_id = str(id['switch']['id'])
        else:
            switch_id = 'null'
        if id['san_switch'] != None:
            san_switch_id = str(id['san_switch']['id'])
        else:
            san_switch_id = 'null'
        if id['storage'] != None:
            storage_id = str(id['storage']['id'])
        else:
            storage_id = 'null'
        if id['firewall'] != None:
            firewall_id = str(id['firewall']['id'])
        else:
            firewall_id = 'null'
        if id['load_balancer'] != None:
            load_balancer_id = str(id['load_balancer']['id'])
        else:
            load_balancer_id = 'null'
          
        data =     {'device_id': [device_id],
                    'device_name': [device_name],
                    'device_type': [device_type],
                    'device_type_manufacture': [device_type_manufacture],
                    'device_role': [device_role],
                    'serial': [serial],
                    'site': [site],
                    'location': [location],
                    'rack': [rack],
                    'status': [status],
                    'primary_ip4': [primary_ip4],
                    'manager_name': [manager_name],
                    'manager_mail': [manager_mail],
                    'switch_id': [ switch_id],
                    'san_switch_id': [san_switch_id],
                    'storage_id': [storage_id],
                    'firewall_id': [firewall_id],
                    'load_balancer_id': [load_balancer_id]}                       
        df = pd.DataFrame(data)           
        try:
            existing_df = pd.read_csv("device_info.csv")
            df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            pass
        df.to_csv("device_info.csv", index=False) 
        
    offset = offset + 50                                       # de offset ngoai vong for se bi lap 3 lan => de offset ben trong


