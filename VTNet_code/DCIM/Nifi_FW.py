import requests
import json
import asyncore
#from asyncio.windows_events import NULL
import pandas as pd
import openpyxl
import mysql.connector
from datetime import datetime

FW_url = 'http://10.255.58.203/api/dcim/firewalls/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",FW_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123456',
                              host='10.254.139.183', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 25
offset= 0

# FW_interface = open("FW_interface.txt", "w+", encoding = 'UTF-8')
while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", FW_url, headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        FW_id = int(id['id'])
        FW_name = str(id['name'])        
        system_id = int(id['system']['id']) if id['system'] is not None else 'null'
        system_name = str(id['system']['display']) if id['system'] is not None else 'null'
        manager = str(id['manager']['username'])

        devices = id.get("devices", [])
        device_ids = [device.get("id") for device in devices]
        device_id1 = device_ids[0] if len(device_ids) > 0 else 'null'
        device_id2 = device_ids[1] if len(device_ids) > 1 else 'null' 

        verify_status = str(id['verify_status']['label'])        

        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # s= str(FW_id) + "|" + FW_name + "|" + str(system_id) + "|" + system_name + "|" +manager + "|" + str(device_id1) + "|" + str(device_id2) + "|" + str(insert_time) +"\n"
        # FW_interface.write(s)

        data =  {'FW_id': [FW_id],
                'FW_name': [FW_name],
                'system_id': [system_id],
                'system_name': [system_name],
                'manager': [manager],
                'device_id1': [device_id1],
                'device_id2': [device_id2],
                'insert_time': [insert_time]}
                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO Firewall (FW_id, FW_name, system_id, system_name, manager, device_id1, device_id2, insert_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" 
            val = (row['FW_id'], row['FW_name'], row['system_id'], row['system_name'], row['manager'], row['device_id1'], row['device_id2'], insert_time)
            cursor.execute(sql, val)
        # df_string = df.to_string(index=False)
        # print(df_string)
        # commit the changes to the database
        cnx.commit()

    offset = offset + 25                                    # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()
print('success')            
