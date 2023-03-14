import requests
import json
import asyncore
from asyncio.windows_events import NULL
import pandas as pd
import openpyxl
import mysql.connector


module_url = 'http://10.255.58.203/api/service/modules/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",module_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123',
                              host='10.205.35.216', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 50
offset= 0

while offset <  250:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", module_url , headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        service_user_id = str(id['service_user']['id'])
        module_id = str(id['id'])
        service_id = str(id['service']['id'])
        if id['group'] != None:
            group_code = str(id['group']['code'])
            group_name = str(id['group']['name'])
        else:
            group_code = 'Không có group code'
            group_name = 'Không có group name'
        module_name = str(id['name'])
        module_code = str(id['code'])
        module_status = str(id['service']['status']['label'])

        # lay thong tin username va instance_id tu api service-users 

        data =  {'Service_id': [service_id],
                'Code': [module_code],
                'Name': [module_name],
                'Module_ID': [module_id],
                'Group_code': [group_code],
                'Group_name': [group_name],
                'Service_user_ID': [service_user_id],
                'Status': [module_status]}                       
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO Module (Module_ID, Service_id, Group_code, Group_name, Code, Name, Service_user_ID, Status) VALUES (%s, %s, %s, %s,%s, %s, %s, %s) ON DUPLICATE KEY UPDATE  Service_id=%s, Group_code=%s, Group_name=%s, Code=%s, Name=%s, Service_user_ID=%s, Status=%s"
            val = (row['Module_ID'], row['Service_id'], row['Group_code'], row['Group_name'], row['Code'], row['Name'], row['Service_user_ID'], row['Status'], row['Service_id'], row['Group_code'], row['Group_name'], row['Code'], row['Name'], row['Service_user_ID'], row['Status'])
            cursor.execute(sql, val)
        
        # commit the changes to the database
        cnx.commit()

    offset = offset + 50                                       # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()
            