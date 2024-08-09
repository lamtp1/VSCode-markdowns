import asyncore
import json
from asyncio.windows_events import NULL
from re import S
import pandas as pd
import openpyxl
import requests
# import mysql.connector

# lay ipv4 primary tu api instance
IPMS_SW_BW_hour_3_url = 'http://192.168.251.20/api/?api=get_int_group_peak&gr=23611'   # neu la CPU thi 'cus', BW thi 'int'


IPMS_SW_BW_hour_3 = open("IPMS_SW_BW_hour_3.txt", "w+", encoding = 'UTF-8')
headers = {
    'Content-Type': "application/json",
    }

# cnx = mysql.connector.connect(user='root', password='123',
#                               host='10.205.35.216', port=3306, database='CPM')
# cursor = cnx.cursor()

rp1 = requests.request("GET",IPMS_SW_BW_hour_3_url, headers=headers).json()
for x in rp1:
    
    id = str(x['id'])
    hostname = str(x['hostname'])
    ip = str(x['ip'])

    name = str(x['name'])
    parts = name.split('-')
    parts = [part.strip() for part in parts]
    name2 = ' '.join(parts[:1])
    
    if x['speed'] != None:
        speed = str(int(x['speed'])/1000)
    else:
        speed = 'null'
    maxi_60 = str(x['maxi_60'])
    maxo_60 = str(x['maxo_60'])
    last_update = str(x['last_update'])
    
    # data =  {   'id': [id],
    #             'hostname': [hostname],
    #             'ip': [ip],
    #             'name': [name2],
    #             'speed': [speed],
    #             'maxi_60': [maxi_60],
    #             'maxo_60': [maxo_60],
    #             'last_update': [last_update]}
                
    # df = pd.DataFrame(data)

    # for index, row in df.iterrows():
    #     sql = "INSERT INTO `IPMS_hour` (id, hostname, ip, name, speed, maxi_60, maxo_60, last_update) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)  "
    #     val = (row['id'], row['hostname'], row['ip'], row['name'],  row['speed'], row['maxi_60'], row['maxo_60'], row['last_update'])
    #     cursor.execute(sql, val)
    
    # df_string = df.to_string(index=False)
    # print(df_string)
    # commit the changes to the database
#     cnx.commit()

# cursor.close()
# cnx.close()

    s = id + "|"  + hostname + "|" + ip + "|" + name2 + "|"  + speed +  "|" + maxi_60 + "|" + maxo_60 +  "|" + last_update  + "\n"
    IPMS_SW_BW_hour_3.write(s)
    
IPMS_SW_BW_hour_3.close()
