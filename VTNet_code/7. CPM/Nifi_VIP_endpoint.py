import requests
import json
import asyncore
from asyncio.windows_events import NULL
import pandas as pd
import openpyxl
import mysql.connector


vip_url = 'http://10.255.58.203/api/dcim/vip-endpoints/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",vip_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123',
                              host='10.205.35.216', port=3306, database='CPM') 
cursor = cnx.cursor()

limit= 250
offset= 0

while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", vip_url , headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        VIP_Endpoint_ID = str(id['id'])
        Code = str(id['code'])
        Name = str(id['name'])
        LB_ID = str(id['load_balancer']['id'])
        VIP_address = str(id['vip']['address'])
        Port = str(id['port'])
        Protocol = str(id['protocol']['label'])
        Status = str(id['status']['label'])
        
        # lay thong tin username va instance_id tu api service-users 

        data =  {'VIP_Endpoint_ID': [VIP_Endpoint_ID],
                'Code': [Code],
                'Name': [Name],
                'LB_ID': [LB_ID],
                'VIP_address': [VIP_address],
                'Port': [Port],
                'Protocol': [Protocol],
                'Status': [Status]}
                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO VIP_Endpoint (VIP_Endpoint_ID, Code, Name, LB_ID, VIP_address, Port, Protocol, Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE  Code=%s, Name=%s, LB_ID=%s, VIP_address=%s, Port=%s, Protocol=%s, Status=%s"
            val = (row['VIP_Endpoint_ID'], row['Code'], row['Name'], row['LB_ID'], row['VIP_address'], row['Port'], row['Protocol'], row['Status'], row['Code'], row['Name'], row['LB_ID'], row['VIP_address'], row['Port'], row['Protocol'], row['Status'])
            cursor.execute(sql, val)
        # df_string = df.to_string(index=False)
        # print(df_string)
        # commit the changes to the database
        cnx.commit()

    offset = offset + 250                                       # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()
