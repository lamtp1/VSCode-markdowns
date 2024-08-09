# -*- coding: iso-8859-1 -*-

import requests
import json
import asyncore
import pandas as pd
import mysql.connector
from datetime import datetime

service_url = 'http://10.255.58.203/api/service/service-owners/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",service_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123456',
                              host='10.254.139.183', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 250
offset= 0

while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", service_url , headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        service_owner_id = str(id['id'])
        Owner_ID = str(id['owner']['id'])
        Service_ID = str(id['service']['id'])
        Owner_name = str(id['owner']['username'])
        Owner_email = str(id['owner']['email'])

        # lay thong tin username va instance_id tu api service-users 

        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data =  {'service_owner_id': [service_owner_id],
                'Owner_ID': [Owner_ID],
                'Service_ID': [Service_ID],
                'Owner_name': [Owner_name],
                'Owner_email': [Owner_email],
                'insert_time': [insert_time]}
                
                
        df = pd.DataFrame(data)     
        for index, row in df.iterrows():
            sql = "INSERT INTO Service_Owner (service_owner_id, Owner_ID, Service_ID, Owner_name, Owner_email, insert_time) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE Service_ID=%s, Owner_ID=%s, Owner_name=%s, Owner_email=%s"
            val = (row['service_owner_id'], row['Owner_ID'], row['Service_ID'], row['Owner_name'], row['Owner_email'], insert_time, row['Owner_ID'], row['Service_ID'], row['Owner_name'], row['Owner_email'])
            cursor.execute(sql, val)
            
        # df_string = df.to_string(index=False)
        # print(df_string)
        # commit the changes to the database
        cnx.commit()

    offset = offset + 250                                       # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()
print('success')