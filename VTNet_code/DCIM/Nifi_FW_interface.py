import requests
import json
import asyncore
#from asyncio.windows_events import NULL
import pandas as pd
import openpyxl
import mysql.connector
from datetime import datetime

FW_int_url = 'http://10.255.58.203/api/dcim/firewall-interfaces/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",FW_int_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123456',
                              host='10.254.139.183', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 250
offset= 0

# FW_interface = open("FW_interface.txt", "w+", encoding = 'UTF-8')
while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", FW_int_url , headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        FW_id = int(id['firewall']['id'])
        FW_name = str(id['firewall']['name'])
        FW_interface_id = int(id['id'])
        FW_interface_name = str(id['name'])

        if id['firewall_zone'] != None:
            FW_int_zone = str(id['firewall_zone']['name'])
        else: 
            FW_int_zone = 'null'    

        if id['vlan_id'] != None:
            Vlan_id = int(id['vlan_id'])
        else:
            Vlan_id = 'null'

        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # s= str(FW_id) + "|" + FW_name + "|" + str(FW_interface_id) + "|" + FW_interface_name + "|" +FW_int_zone + "|" + str(Vlan_id) +"\n"
        # FW_interface.write(s)

        data =  {'FW_id': [FW_id],
                'FW_name': [FW_name],
                'FW_interface_id': [FW_interface_id],
                'FW_interface_name': [FW_interface_name],
                'FW_int_zone': [FW_int_zone],
                'Vlan_id': [Vlan_id],
                'insert_time': [insert_time]}
                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO Firewall_interface (FW_id, FW_name, FW_interface_id, FW_interface_name, FW_int_zone, Vlan_id, insert_time) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE FW_id=%s, FW_name=%s, FW_interface_id=%s, FW_interface_name=%s" 
            val = (row['FW_id'], row['FW_name'], row['FW_interface_id'], row['FW_interface_name'], row['FW_int_zone'], row['Vlan_id'], insert_time)
            cursor.execute(sql, val)
        # df_string = df.to_string(index=False)
        # print(df_string)
        # commit the changes to the database
        cnx.commit()

    offset = offset + 250                                    # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()
print('success')            
