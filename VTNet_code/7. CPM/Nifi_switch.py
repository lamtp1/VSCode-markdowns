import requests
import json
import asyncore
from asyncio.windows_events import NULL
import pandas as pd
import openpyxl
import mysql.connector


switch_url = 'http://10.255.58.203/api/dcim/switches/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",switch_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123',
                              host='10.205.35.216', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 250
offset= 0
switch_file = open ("switch_file.txt", "w+", encoding = 'UTF-8')
while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", switch_url , headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        Switch_ID = str(id['id'])
        rp3 = requests.request("GET", switch_url + Switch_ID, headers=headers).json()
        Group_name = str(rp3['group']['name'])
        Vlan_group = str(rp3['group']['vlan_group'])
        Platform = str(rp3['platform']['label'])
        Type = str(rp3['type']['label'])
        Layer = str(rp3['layer']['label'])
        Firmware_version = str(rp3['firmware_version'])
        Manager_name = str(rp3['manager']['username'])
        Manager_email = str(rp3['manager']['email'])
        Verify_status =  str(rp3['verify_status']['label'])

        # s = Switch_ID + "|" + Group_name + "|" + Vlan_group + "|" + Platform + "|" + Type + "|" + Layer + "|" + Firmware_version + "|" + Manager_name + "|" + Manager_email + "|" + Verify_status + "\n"
        # switch_file.write(s)
        # lay thong tin username va instance_id tu api service-users 

        data =  {'Switch_ID': [Switch_ID],
                'Group_name': [Group_name],
                'Vlan_group': [Vlan_group],
                'Platform': [Platform],
                'Type': [Type],
                'Layer': [Layer],
                'Firmware_version': [Firmware_version],
                'Manager_name': [Manager_name],
                'Manager_email': [Manager_email],
                'Verify_status': [Verify_status]}
                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO Switch (Switch_ID, Group_name, Vlan_group, Platform, Type, Layer, Firmware_version, Manager_name, Manager_email, Verify_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE  Group_name=%s, Vlan_group=%s, Platform=%s, Type=%s, Layer=%s, Firmware_version=%s, Manager_name=%s, Manager_email=%s, Verify_status=%s"
            val = (row['Switch_ID'], row['Group_name'], row['Vlan_group'], row['Platform'], row['Type'], row['Layer'], row['Firmware_version'], row['Manager_name'], row['Manager_email'], row['Verify_status'], row['Group_name'], row['Vlan_group'], row['Platform'], row['Type'], row['Layer'], row['Firmware_version'], row['Manager_name'], row['Manager_email'], row['Verify_status'])
            cursor.execute(sql, val)
        df_string = df.to_string(index=False)
        print(df_string)
        # commit the changes to the database
        cnx.commit()

    offset = offset + 250                                       # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()
switch_file.close()