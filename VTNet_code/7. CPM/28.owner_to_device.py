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

limit= 250
offset= 0
device_owner = open("Device_Owner_ver6.txt", "w+", encoding='UTF-8')
while offset <  ip_count:
    querystring = {"limit":limit, "offset": offset}
    rp2= requests.request("GET", device_url, headers=headers, params=querystring).json()['results']
    names = ["duongvt3","anhnv138", "namnv80", "hungdq27", "hungtq35", "minhbd"]
    for id in rp2:
        if str(id['manager']['username']) in names:
            device_id = str(id["id"])
            device_role = str(id['device_role']['name'])
            manager_name = str(id['manager']['username'])
            if id['primary_ip4'] != None:
                ip = str(id['primary_ip4']['address'])
            else:
                ip = 'None'
            device_name = str(id['name'])
            device_manufacturer = str(id['device_type']['manufacturer']['display'])
            tenant = str(id['tenant']['name'])
            site = str(id['site']['name'])

            s = device_id + "|" + device_role + "|" + manager_name + "|" + ip + "|" + device_name + "|" + device_manufacturer + "|" + tenant + "|" + site +  "\n"
            device_owner.write(s)
        # data =     {'Loai Thiet Bi': [device_role],
        #             'Nguoi quan ly': [manager_name]}                       
        # df = pd.DataFrame(data)           
        # try:
        #     existing_df = pd.read_excel("device_owner.xlsx")
        #     df = pd.concat([existing_df, df], ignore_index=True)
        # except FileNotFoundError:
        #     pass
        # df.to_excel("device_owner.xlsx", index=False) 
        
    offset = offset + 250                                      # de offset ngoai vong for se bi lap 3 lan => de offset ben trong
device_owner.close()

