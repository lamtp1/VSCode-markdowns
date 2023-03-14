import requests
import json
import asyncore
from asyncio.windows_events import NULL
import pandas as pd
import openpyxl
import mysql.connector


service_url = 'http://10.255.58.203/api/service/service-owners/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",service_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123',
                              host='10.205.35.216', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 50
offset= 0

while offset <  250:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", service_url , headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        Owner_ID = str(id['owner']['id'])
        Service_ID = str(id['service']['id'])
        Owner_name = str(id['owner']['last_name'])
        Owner_mail = str(id['owner']['email'])

        # lay thong tin username va instance_id tu api service-users 

        data =  {'Owner_ID': [Owner_ID],
                'Service_ID': [Service_ID],
                'Owner_name': [Owner_name],
                'Owner_mail': [Owner_mail]}
                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO Service (Owner_ID, Service_ID, Owner_name, Owner_mail) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE  Owner_ID=%s, Owner_name=%s, Owner_mail=%s"
            val = (row['Owner_ID'], row['Service_ID'], row['Owner_name'], row['Owner_mail'], row['Owner_ID'], row['Owner_name'], row['Owner_mail'])
        
        # df_string = df.to_string(index=False)
        # print(df_string)
        # commit the changes to the database
        cnx.commit()

    offset = offset + 50                                       # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()
