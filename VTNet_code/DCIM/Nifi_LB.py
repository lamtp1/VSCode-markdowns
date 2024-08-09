import requests
import json
import asyncore
#from asyncio.windows_events import NULL
import pandas as pd
import openpyxl
import mysql.connector
from datetime import datetime

LB_url = 'http://10.255.58.203/api/dcim/load-balancers/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",LB_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123456',
                              host='10.254.139.183', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 20
offset= 0

while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", LB_url , headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        LB_ID = int(id['id'])
        System = str(id['system'])
        Code = str(id['code'])
        Name = str(id['name'])
        Site = str(id['site']['name'])
        LB_type = str(id['lb_type']['label'])
        Manager_name = str(id['manager']['username'])
        Manager_email = str(id['manager']['email'])
        Verify_status =  str(id['verify_status']['label'])
        # lay thong tin username va instance_id tu api service-users 

        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data =  {'LB_ID': [LB_ID],
                'System': [System],
                'Code': [Code],
                'Name': [Name],
                'Site': [Site],
                'LB_type': [LB_type],
                'Manager_name': [Manager_name],
                'Manager_email': [Manager_email],
                'Verify_status': [Verify_status],
                'insert_time': [insert_time]}
                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO LB (LB_ID, System, Code, Name, Site, LB_type, Manager_name, Manager_email, Verify_status, insert_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE  System=%s, Code=%s, Name=%s, Site=%s, LB_type=%s, Manager_name=%s, Manager_email=%s, Verify_status=%s"
            val = (row['LB_ID'], row['System'], row['Code'], row['Name'], row['Site'], row['LB_type'], row['Manager_name'], row['Manager_email'], row['Verify_status'], insert_time, row['System'], row['Code'], row['Name'], row['Site'], row['LB_type'], row['Manager_name'], row['Manager_email'], row['Verify_status'])
            cursor.execute(sql, val)
        # df_string = df.to_string(index=False)
        # print(df_string)
        # commit the changes to the database
        cnx.commit()

    offset = offset + 20                                    # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()
print('success')            
