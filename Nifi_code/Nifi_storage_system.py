import requests
import json
import asyncore
from asyncio.windows_events import NULL
import pandas as pd
import openpyxl
import mysql.connector


Storage_system_url = 'http://10.255.58.203/api/dcim/storage-systems/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",Storage_system_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123',
                              host='10.205.35.216', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 250
offset= 0

while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", Storage_system_url , headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        Storage_System_ID = int(id['id'])
        Name = str(id["name"])
        Manufacturer = str(id['manufacturer']['label'])
        Type = str(id['type']['label'])
        Tenant = str(id['tenant']["name"])
        Manager_name = str(id['manager']['username'])
        Manager_email = str(id['manager']['email'])
        Total_space = str(id['total_space'])
        Used_space = str(id['used_space'])
        Free_space = str(id['free_space'])

        # lay thong tin username va instance_id tu api service-users 

        data =  {'Storage_System_ID': [Storage_System_ID],
                'Name': [Name],
                'Manufacturer': [Manufacturer],
                'Type': [Type],
                'Tenant': [Tenant],
                'Manager_name': [Manager_name],
                'Manager_email': [Manager_email],
                'Total_space': [Total_space],
                'Used_space': [Used_space],
                'Free_space': [Free_space]}
                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO Storage_System (Storage_System_ID, Name, Manufacturer, Type, Tenant, Manager_name, Manager_email, Total_space, Used_space, Free_space) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE  Name=%s, Manufacturer=%s, Type=%s, Tenant=%s, Manager_name=%s, Manager_email=%s, Total_space=%s, Used_space=%s, Free_space=%s"
            val = (row['Storage_System_ID'], row['Name'], row['Manufacturer'], row['Type'], row['Tenant'],  row['Manager_name'], row['Manager_email'], row['Total_space'], row['Used_space'], row['Free_space'], row['Name'], row['Manufacturer'], row['Type'], row['Tenant'],  row['Manager_name'], row['Manager_email'], row['Total_space'], row['Used_space'], row['Free_space'])
            cursor.execute(sql, val)
        # df_string = df.to_string(index=False)
        # print(df_string)
        # commit the changes to the database
        cnx.commit()

    offset = offset + 250                                       # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()
            