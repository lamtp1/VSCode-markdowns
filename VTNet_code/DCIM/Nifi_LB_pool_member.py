import requests
import json
import asyncore
import pandas as pd
import mysql.connector
from datetime import datetime

LB_pool_member_url = 'http://10.255.58.203/api/dcim/lb-pool-members/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",LB_pool_member_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123456',
                              host='10.254.139.183', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 250
offset= 0
# lb_pool_member = open("pool_members_file.txt", "w+", encoding = 'UTF-8')
while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", LB_pool_member_url , headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        LB_pool_member_ID = str(id['id'])
        LB_pool_ID = str(id["lb_pool"]["id"])
        Primary_ip4 = str(id['ip_address']['display'])
        Name = str(id['name'])
        Status = str(id['status']['label'])
        # lay thong tin username va instance_id tu api service-users 

        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data =  {'LB_pool_member_ID': [LB_pool_member_ID],
                'LB_pool_ID': [LB_pool_ID],
                'Primary_ip4': [Primary_ip4],
                'Name': [Name],
                'Status': [Status],
                'insert_time': [insert_time]}
                
        # s = LB_pool_member_ID + "|" + LB_pool_ID + "|" + Primary_ip4 + "|" + Name + "|" + Status + "\n"
        # lb_pool_member.write(s)
        
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO LB_pool_member (LB_pool_member_ID, LB_pool_ID, Primary_ip4, Name, Status, insert_time) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE   Primary_ip4=%s, Name=%s, Status=%s"
            val = (row['LB_pool_member_ID'], row['LB_pool_ID'], row['Primary_ip4'], row['Name'], row['Status'], insert_time, row['Primary_ip4'], row['Name'], row['Status'])
            cursor.execute(sql, val)
        # df_string = df.to_string(index=False)
        # print(df_string)
        # commit the changes to the database
        cnx.commit()

    offset = offset + 250                                       # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()
# lb_pool_member.close()      
print('success')