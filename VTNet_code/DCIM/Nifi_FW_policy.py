import requests
import json
import asyncore
#from asyncio.windows_events import NULL
import pandas as pd
import openpyxl
import mysql.connector
from datetime import datetime

FW_policy_url = 'http://10.255.58.203/api/dcim/firewall-policies/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",FW_policy_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123456',
                              host='10.254.139.183', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 250
offset= 0

# FW_interface = open("FW_interface.txt", "w+", encoding = 'UTF-8')
# x = "FW_id|FW_name|source_zone|dest_zone|insert_time \n"
# FW_interface.write(x)
while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", FW_policy_url, headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        policy_id = id['id']
        FW_id = int(id['firewall']['id'])
        FW_name = str(id['firewall']['name']) 

        source_zones = id.get("srczone", [])
        source_display = [source_display.get("display") for source_display in source_zones]
        source_zone = source_display[0] if len(source_display) > 0 else None

        dest_zones = id.get("dstzone", [])
        dest_display = [dest_display.get("display") for dest_display in dest_zones]
        dest_zone = dest_display[0] if len(dest_display) > 0 else None    

        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        s= str(FW_id) + "|" + FW_name + "|" +  source_zone + "|" +dest_zone + "|" + str(insert_time) +"\n"
        # FW_interface.write(s)

        data =  {'FW_id': [FW_id],
                'FW_name': [FW_name],
                'source_zone': [source_zone],
                'dest_zone': [dest_zone],
                'insert_time': [insert_time]}
                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO Firewall_policy (FW_id, FW_name, source_zone, dest_zone, insert_time) VALUES (%s, %s, %s, %s, %s)" 
            val = (row['FW_id'], row['FW_name'], row['source_zone'], row['dest_zone'], insert_time)
            cursor.execute(sql, val)

        # commit the changes to the database
        cnx.commit()

    offset = offset + 250                                    # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()
print('success')            
