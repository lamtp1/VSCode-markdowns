import requests
import json
import asyncore
from asyncio.windows_events import NULL
import pandas as pd
import openpyxl
import mysql.connector

volume_url = 'http://10.255.58.203/api/dcim/volumes/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",volume_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123',
                              host='10.205.35.216', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 250
offset= 0

while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", volume_url , headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        Volume_ID = str(id['id'])
        Pool_ID = str(id["pool"]["id"])
        Pool_name = str(id["pool"]["name"])
        # lay thong tin username va instance_id tu api service-users 

        data =  {'Volume_ID': [Volume_ID],
                'Pool_ID': [Pool_ID],
                'Pool_name': [Pool_name]}
                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO Volume (Volume_ID, Pool_ID, Pool_name) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE  Pool_ID=%s, Pool_name=%s"
            val = (row['Volume_ID'], row['Pool_ID'], row['Pool_name'], row['Pool_ID'], row['Pool_name'])
            cursor.execute(sql, val)
        df_string = df.to_string(index=False)
        print(df_string)
        # commit the changes to the database
        cnx.commit()

    offset = offset + 250                                       # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()
            