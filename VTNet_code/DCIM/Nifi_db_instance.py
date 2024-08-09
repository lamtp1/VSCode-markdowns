import requests
import json
import asyncore
import pandas as pd
import mysql.connector
from datetime import datetime

db_instance_url = 'http://10.255.58.203/api/database/db-instances/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",db_instance_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123456',
                              host='10.254.139.183', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 250
offset= 0

while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", db_instance_url , headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        DB_instance_ID = str(id['id'])
        Database_ID = str(id['database']['id'])
        Manager_name = str(id['database']['manager']['username'])
        Manager_mail = str(id['database']['manager']['email'])
        Instance_ID = str(id['instance']['id'])
        # lay thong tin username va instance_id tu api service-users 

        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        data =  {'DB_instance_ID': [DB_instance_ID],
                'Database_ID': [Database_ID],
                'Manager_name': [Manager_name],
                'Manager_email': [Manager_mail],
                'Instance_ID': [Instance_ID],
                'insert_time': [insert_time]}
                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO Database_instance (DB_instance_ID, Database_ID, Manager_name, Manager_email, Instance_ID, insert_time) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE  Database_ID=%s, Manager_name=%s, Manager_email=%s, Instance_ID=%s"
            val = (row['DB_instance_ID'], row['Database_ID'], row['Manager_name'], row['Manager_email'], row['Instance_ID'], insert_time, row['Database_ID'], row['Manager_name'], row['Manager_email'], row['Instance_ID'])
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
