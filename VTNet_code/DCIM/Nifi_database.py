import requests
import json
import asyncore
import pandas as pd
# import openpyxl
import mysql.connector
from datetime import datetime

database_url = 'http://10.255.58.203/api/database/databases/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",database_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123456',
                              host='10.254.139.183', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 250
offset= 0

while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", database_url , headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        Database_ID = str(id['id'])
        Name = str(id['name'])
        Type = str(id['type']['label'])
        Service_name = str(id['service_name'])
        if id['scan_ip'] != None:
            Scan_ip = str(id['scan_ip']['display'])
        else:
            Scan_ip = "Nothing"
        if id['version'] != None:
            Version = str(id["version"]["name"])
        else:
            Version = "Nothing"
        Status = str(id["status"]["label"])
        Level_importance = str(id['level_important']['label'])
        Manager_name = str(id['manager']['username'])
        Manager_email = str(id['manager']['email'])
        Tenant = str(id['tenant']['name'])
        Monitored = str(id['monitored']['label'])
        Verify_status = str(id['verify_status']['label'])
        # lay thong tin username va instance_id tu api service-users 

        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data =  {'Database_ID': [Database_ID],
                'Name': [Name],
                'Type': [Type],
                'Service_name': [Service_name],
                'Scan_ip': [Scan_ip],
                'Version': [Version],
                'Status': [Status],
                'Level_importance': [Level_importance],
                'Manager_name': [Manager_name],
                'Manager_email': [Manager_email],
                'Tenant': [Tenant],
                'Monitored': [Monitored],
                'Verify_status': [Verify_status],
                'insert_time': [insert_time]}
                
        df = pd.DataFrame(data)

        for index, row in df.iterrows():
            sql = "INSERT INTO `Database` (Database_ID, Name, Type, Service_name, Scan_ip, Version, Status, Level_importance, Manager_name, Manager_email, Tenant, Monitored, Verify_status, insert_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  ON DUPLICATE KEY UPDATE Name=%s, Type=%s, Service_name=%s, Scan_ip=%s, Version=%s, Status=%s, Level_importance=%s, Manager_name=%s, Manager_email=%s, Tenant=%s, Monitored=%s, Verify_status=%s"
            val = (row['Database_ID'], row['Name'], row['Type'], row['Service_name'], row['Scan_ip'], row['Version'], row['Status'], row['Level_importance'], row['Manager_name'], row['Manager_email'], row['Tenant'], row['Monitored'], row['Verify_status'], insert_time, row['Name'], row['Type'], row['Service_name'], row['Scan_ip'], row['Version'], row['Status'], row['Level_importance'], row['Manager_name'], row['Manager_email'], row['Tenant'], row['Monitored'], row['Verify_status'])
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
