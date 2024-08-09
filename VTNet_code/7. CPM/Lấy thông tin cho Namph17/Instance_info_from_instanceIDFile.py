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

# temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }
# rp1 = requests.request("GET",instance_url, headers=headers, params=temp_qr)
# ip_count = rp1.json()['count']

# limit= 50
# offset= 0
instance_file = open("ip_to_id.txt", "r", encoding='UTF-8')
instance_info = open("thong_tin_instance.txt", "w", encoding='UTF-8')
# while offset <  250:
#     querystring = {"limit":limit, "offset": offset}
#     rp2= requests.request("GET",instance_url, headers=headers, params=querystring).json()['results']
for id in instance_file:
    rp2= requests.request("GET",instance_url+id, headers=headers).json()
    if rp2['primary_ip4'] != None:
        instance_id = str(rp2['id'])
        primary_ip4 = str(rp2['primary_ip4']['address'])      # dung tai primary_ip thi chi co 1 ip
        cloud_instance_uuid = str(rp2['cloud_instance_uuid'])
    
        # data =  {'instance_id': [instance_id],
        #             'Name': [instance_name],
        #             'Device_id': [device_id],
        #             'Parent_instance': [parent_instance],
        #             'Manager_first_name': [owner_name],
        #             'Manager_mail': [owner_mail],
        #             'tenant': [tenant],
        #             'Type': [Type],
        #             'Status': [status],
        #             'Level_importance': [level_important],
        #             'Monitored': [monitored],
        #             'primary_ip4': [primary_ip4],
        #             'primary_ip6': [primary_ip6]}                       
        # df = pd.DataFrame(data)           
        # try:
        #     existing_df = pd.read_excel("thong_tin_instance.xlsx")
        #     df = pd.concat([existing_df, df], ignore_index=True)
        # except FileNotFoundError:
        #     pass
        # df.to_excel("thong_tin_instance.xlsx", index=False) 
        
        s = cloud_instance_uuid + '|' + instance_id + '|'+ primary_ip4 + '\n' 
        instance_info.write(s)

# offset = offset + 50                                       # de offset ngoai vong for se bi lap 3 lan => de offset ben trong
instance_file.close()
instance_info.close()

