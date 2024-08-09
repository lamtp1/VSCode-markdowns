import requests
import json
import asyncore
#from asyncio.windows_events import NULL
import pandas as pd
import openpyxl
import mysql.connector
from datetime import datetime

FW_route_url = 'http://10.255.58.203/api/dcim/firewall-routes/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",FW_route_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123456',
                              host='10.254.139.183', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 250
offset= 0

# FW_interface = open("FW_interface.txt", "w+", encoding = 'UTF-8')
# x = "FW_id|FW_name|gateway_ip|interface_name|dst_prefix|dst_address|device_id1|device_id2|insert_time \n"
# FW_interface.write(x)
while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", FW_route_url, headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        FW_id = int(id['firewall']['id'])
        FW_name = str(id['firewall']['name'])        
        device_id1 = id['firewall']['devices'][0] if len(id['firewall']['devices']) > 0 else 'null'
        device_id2 = id['firewall']['devices'][1] if len(id['firewall']['devices']) > 1 else 'null'
        dst_prefix = str(id['dst_prefix']['display']) if id['dst_prefix'] is not None else 'null'
        dst_address = str(id['dst_address']['display']) if id['dst_address'] is not None else 'null'
        interface_name = str(id['interface']['name']) if id['interface'] is not None else 'null'
        gateway_ip = str(id['gateway']['display']) if id['gateway'] is not None else 'null'    

        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # s= str(FW_id) + "|" + FW_name + "|" + str(gateway_ip) + "|" + str(interface_name) + "|" + dst_prefix + "|" +dst_address + "|" + str(device_id1) + "|" + str(device_id2) + "|" + str(insert_time) +"\n"
        # FW_interface.write(s)

        data =  {'FW_id': [FW_id],
                'FW_name': [FW_name],
                'device_id1': [device_id1],
                'device_id2': [device_id2],
                'dst_prefix': [dst_prefix],
                'dst_address': [dst_address],
                'interface_name': [interface_name],
                'gateway_ip': [gateway_ip],
                'insert_time': [insert_time]}
                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO Firewall_routes (FW_id, FW_name, device_id1, device_id2, dst_prefix, dst_address, interface_name, gateway_ip, insert_time ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)" 
            val = (row['FW_id'], row['FW_name'], row['device_id1'], row['device_id2'], row['dst_prefix'], row['dst_address'], row['interface_name'], row['gateway_ip'], insert_time)
            cursor.execute(sql, val)
        # commit the changes to the database
        cnx.commit()

    offset = offset + 250                                    # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()
print('success')            
