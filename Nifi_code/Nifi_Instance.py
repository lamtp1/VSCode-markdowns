import asyncore
import json
from asyncio.windows_events import NULL
from re import S
import pandas as pd
import openpyxl
import requests
import mysql.connector

# lay ipv4 primary tu api instance
instance_url = 'http://10.255.58.203/api/dcim/instances/'
site_url = 'http://10.255.58.203/api/dcim/devices/'
owner_url = 'http://10.255.58.203/api/service/service-owners/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }
rp1 = requests.request("GET",instance_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123',
                              host='10.205.35.216', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 250
offset= 0

while offset <  ip_count:
    querystring = {"limit":limit, "offset": offset}
    rp2= requests.request("GET",instance_url, headers=headers, params=querystring).json()['results']
    for id in rp2:
        if id['primary_ip4'] != None:
            instance_id = int(id['id'])
            instance_name = str(id['name'])
            if id['device'] != None:
                device_id = int(id['device']['id'])
            else:
                device_id = None
            if id['parent_instance'] != None:
                parent_instance = str(id['parent_instance']['id'])
            else:
                parent_instance = 'null'
            owner_name = str(id["manager"]["username"])
            owner_mail = str(id["manager"]["email"])
            if id['tenant'] != None:
                tenant = str(id['tenant']['name'])
            else:
                tenant = 'null'
            Type = str(id['type']['label'])
            status = str(id['status']['label'])
            level_important = str(id['level_important']['label'])
            monitored = str(id['monitored']['label'])
            primary_ip4 = str(id['primary_ip4']['address'])      # dung tai primary_ip thi chi co 1 ip
            primary_ip6 = 'null'
            
        
            data =  {'Instance_ID': [instance_id],
                     'Instance_name': [instance_name],
                     'Device_ID': [device_id],
                     'Parent_instance': [parent_instance],
                     'Manager_name': [owner_name],
                     'Manager_mail': [owner_mail],
                     'Manager_tenant': [tenant],
                     'Type': [Type],
                     'Status': [status],
                     'Level_importance': [level_important],
                     'Monitored': [monitored],
                     'Primary_ip4': [primary_ip4],
                     'Primary_ip6': [primary_ip6]}                       
            df = pd.DataFrame(data)           
            for index, row in df.iterrows():
                sql = "INSERT INTO Instance (Instance_ID, Instance_name, Device_ID, Parent_instance, Manager_name, Manager_mail, Manager_tenant, Type, Status, Level_importance, Monitored, Primary_ip4, Primary_ip6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE  Device_ID=%s, Parent_instance=%s, Manager_name=%s, Manager_mail=%s, Manager_tenant=%s, Type=%s, Status=%s, Level_importance=%s, Monitored=%s, Primary_ip6=%s"
                val = (row['Instance_ID'], row['Instance_name'], row['Device_ID'], row['Parent_instance'], row['Manager_name'], row['Manager_mail'], row['Manager_tenant'], row['Type'], row['Status'], row['Level_importance'], row['Monitored'], row['Primary_ip4'], row['Primary_ip6'], row['Device_ID'], row['Parent_instance'], row['Manager_name'], row['Manager_mail'], row['Manager_tenant'], row['Type'], row['Status'], row['Level_importance'], row['Monitored'], row['Primary_ip6'])
                cursor.execute(sql, val)
            
            # df_string = df.to_string(index=False)
            # print(df_string)
            # commit the changes to the database
            cnx.commit()

    offset = offset + 250                                      # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()

