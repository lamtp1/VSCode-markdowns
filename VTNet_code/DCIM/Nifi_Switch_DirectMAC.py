import requests
import json
import asyncore
import mysql.connector
import pandas as pd
from datetime import datetime

switch_url = 'http://10.255.58.203/api/dcim/switch-drc-objects/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

cnx = mysql.connector.connect(user='root', password='123456',
                              host='10.254.139.183', port=3306, database='CPM')
cursor = cnx.cursor()
rp1 = requests.request("GET",switch_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']


limit= 250
offset= 0

while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp3 = requests.request("GET", switch_url , headers=headers, params=qr_param).json()['results']
    for id in rp3:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        Sw_Drc_Object_ID = str(id['id'])
        Sw_ID = str(id['switch']['id'])
        Interface_name = str(id['interface']['name'])
        Neighbor_MAC = str(id['neighbor_mac'])
        if id['neighbor_interface'] != None:
            if id['neighbor_interface']['device'] != None:
                Neighbor_device_ID = str(id['neighbor_interface']['device']['id'])
            else:
                Neighbor_device_ID = 'null'
            if id['neighbor_interface']['instance'] != None:
                Neighbor_instance_ID = str(id['neighbor_interface']['instance']['id'])
            else:
                Neighbor_instance_ID = 'null'

            insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            data =  {'Sw_Drc_Object_ID': [Sw_Drc_Object_ID],
                    'Sw_ID': [Sw_ID],
                    'Interface_name': [Interface_name],
                    'Neighbor_MAC': [Neighbor_MAC],
                    'Neighbor_device_ID': [Neighbor_device_ID],
                    'Neighbor_instance_ID': [Neighbor_instance_ID],
                    'insert_time': [insert_time]}                
            df = pd.DataFrame(data)           
            for index, row in df.iterrows():
                sql = "INSERT INTO Switch_DiractMAC (Sw_Drc_Object_ID, Sw_ID, Interface_name, Neighbor_MAC, Neighbor_device_ID, Neighbor_instance_ID, insert_time) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE  Sw_Drc_Object_ID=%s, Sw_ID=%s, Interface_name=%s, Neighbor_MAC=%s, Neighbor_device_ID=%s, Neighbor_instance_ID=%s"
                val = (row['Sw_Drc_Object_ID'], row['Sw_ID'], row['Interface_name'], row['Neighbor_MAC'], row['Neighbor_device_ID'], row['Neighbor_instance_ID'], insert_time, row['Sw_Drc_Object_ID'], row['Sw_ID'], row['Interface_name'], row['Neighbor_MAC'], row['Neighbor_device_ID'], row['Neighbor_instance_ID'])
                cursor.execute(sql, val)

            cnx.commit()

    offset = offset + 250                                       # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

print('Done')
cursor.close()
cnx.close()
