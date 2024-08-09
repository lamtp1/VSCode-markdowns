import requests
import json
import asyncore
from asyncio.windows_events import NULL
import pandas as pd
import openpyxl
import mysql.connector


LB_pool_url = 'http://10.255.58.203/api/dcim/lb-pools/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",LB_pool_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123',
                              host='10.205.35.216', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 250
offset= 0
lb_pool = open("lb_pool.txt", "w+", encoding = 'UTF-8')
while offset <  250:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", LB_pool_url , headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        LB_pool_ID = str(id['id'])
        Code = str(id['code'])
        Vip_Endpoint_ID = str(id['vip_endpoint']['id'])
        Algorithm = str(id['algorithm']['label'])
        Protocol = str(id['protocol']['label'])
        Status = str(id['status']['label'])
        # lay thong tin username va instance_id tu api service-users 

        s= LB_pool_ID + "|" + Code + "|" + Vip_Endpoint_ID + "|" + Algorithm + "|" +Protocol + "|" + Status +"\n"
        lb_pool.write(s)
        data =  {'LB_pool_ID': [LB_pool_ID],
                'Code': [Code],
                'Vip_Endpoint_ID': [Vip_Endpoint_ID],
                'Algorithm': [Algorithm],
                'Protocol': [Protocol],
                'Status': [Status]}
                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO LB_pool (LB_pool_ID, Code, Vip_Endpoint_ID, Algorithm, Protocol, Status) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE  Code=%s, Vip_Endpoint_ID=%s, Algorithm=%s, Protocol=%s, Status=%s"
            val = (row['LB_pool_ID'], row['Code'], row['Vip_Endpoint_ID'], row['Algorithm'], row['Protocol'], row['Status'], row['Code'], row['Vip_Endpoint_ID'], row['Algorithm'], row['Protocol'], row['Status'])
            cursor.execute(sql, val)
            
        df_string = df.to_string(index=False)
        print(df_string)
        # commit the changes to the database
        cnx.commit()
        
    offset = offset + 250                                       # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()
lb_pool.close()
            