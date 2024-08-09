import requests
import json
import asyncore
from asyncio.windows_events import NULL
import pandas as pd
import openpyxl
import mysql.connector


service_url = 'http://10.255.58.203/api/service/services/'

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
service_file = open("service_file.txt", "w+", encoding = 'UTF-8')
while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", service_url , headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        service_id = str(id['id'])
        service_code = str(id['code'])
        service_name = str(id['name'])
        if id['service_group'] != None:
            group_code = str(id['service_group']['code'])
        else:
            group_code = 'Null'
        service_status = str(id['status']['label'])
        service_tenant = str(id['tenant']['name'])

        s = service_id + "|" + service_code + "|" + service_name + "|" + group_code + "|" + service_status + "|" + service_tenant+"\n"
        service_file.write(s)
        # print(s)
        # lay thong tin username va instance_id tu api service-users 

        data =  {'Service_ID': [service_id],
                'Code': [service_code],
                'Service_name': [service_name],
                'Service_group': [group_code],
                'Status': [service_status],
                'Tenant': [service_tenant]}
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO Service (Service_ID, Code, Service_name, Service_group, Status, Tenant) VALUES (%s, %s, %s, %s,%s, %s) ON DUPLICATE KEY UPDATE  Code=%s, Service_name=%s, Service_group=%s, Status=%s, Tenant=%s"
            val = (row['Service_ID'], row['Code'], row['Service_name'], row['Service_group'], row['Status'], row['Tenant'],  row['Code'], row['Service_name'], row['Service_group'], row['Status'], row['Tenant'])
            cursor.execute(sql, val)
        # df_string = df.to_string(index=False)
        # print(df_string)
        # commit the changes to the database
        cnx.commit()

    offset = offset + 250                                       # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()
service_file.close()