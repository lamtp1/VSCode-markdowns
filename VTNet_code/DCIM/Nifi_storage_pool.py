import requests
import json
import asyncore
import pandas as pd
import mysql.connector
from datetime import datetime

Storage_pool_url = 'http://10.255.58.203/api/dcim/storage-pools/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",Storage_pool_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123456',
                              host='10.254.139.183', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 250
offset= 0

while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", Storage_pool_url , headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        Pool_ID = str(id['id'])
        Storage_ID = str(id["storage"]["id"])
        Total_space = str(id['total_space'])
        Used_space = str(id['used_space'])
        Free_space = str(id['free_space'])

        # lay thong tin username va instance_id tu api service-users 

        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data =  {'Pool_ID': [Pool_ID],
                'Storage_ID': [Storage_ID],
                'Total_space': [Total_space],
                'Used_space': [Used_space],
                'Free_space': [Free_space],
                'insert_time': [insert_time]}
                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO Storage_Pool (Pool_ID, Storage_ID, Total_space, Used_space, Free_space, insert_time) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE  Storage_ID=%s, Total_space=%s, Used_space=%s, Free_space=%s"
            val = (row['Pool_ID'], row['Storage_ID'], row['Total_space'], row['Used_space'], row['Free_space'], insert_time, row['Storage_ID'], row['Total_space'], row['Used_space'], row['Free_space'])
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
