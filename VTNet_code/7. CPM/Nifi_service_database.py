import requests
import json
import asyncore
from asyncio.windows_events import NULL
import pandas as pd
import openpyxl
import mysql.connector


service_url = 'http://dcim.viettel.vn/api/service/service-databases/'

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

limit= 250
offset= 0
service_file = open("DichVu_DB.txt", "w+", encoding = 'UTF-8')
while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", service_url , headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        ID = str(id['id'])
        service_id = str(id['service']['id'])
        database_id = str(id['database']['id'])
        database_name = str(id['database']['name'])
        database_username = str(id['username'])

        s = ID + "|" + service_id + "|" + database_id + "|" + database_name + "|" + database_username + "\n"
        service_file.write(s)

        data =  {'ID': [ID],
                'service_id': [service_id],
                'database_id': [database_id],
                'database_name': [database_name],
                'database_username': [database_username]
                }
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO service_database (ID, service_id, database_id, database_name, database_username) VALUES (%s, %s, %s, %s,%s) "
            val = (row['ID'], row['service_id'], row['database_id'], row['database_name'], row['database_username'], row['Tenant'])
            cursor.execute(sql, val)
        # df_string = df.to_string(index=False)
        # print(df_string)
        # commit the changes to the database
        cnx.commit()

    offset = offset + 250                        

cursor.close()
cnx.close()
service_file.close()