import asyncore
import json
from asyncio.windows_events import NULL
from re import S
import pandas as pd
import openpyxl
import requests

# lay ipv4 primary tu api instance
device_url = 'http://10.255.58.203/api/dcim/devices/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }
rp1 = requests.request("GET",device_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

# connect to the database
cnx = mysql.connector.connect(user='root', password='123',
                              host='10.205.35.216', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 50
offset= 0
while offset <  250:
    querystring = {"limit":limit, "offset": offset}
    rp2= requests.request("GET", device_url, headers=headers, params=querystring).json()['results']
    for id in rp2:
        device_id = str(id['id'])
        device_name = str(id['name'])
        device_type = str(id['device_type']['display'])
        device_type_manufacture = str(id['device_type']['manufacturer']['display'])
        device_role = str(id['device_role']['display'])
        serial = str(id['serial'])
        site = str(id['site']['name'])
        if id['location'] != None:
            location = str(id['location']['display'])
        else:
            location = 'null'
        if id['rack'] != None:
            rack = str(id['rack']['display'])
        else:
            rack = 'null'
        status = str(id['status']['label'])
        if id['primary_ip4'] != None:
            primary_ip4 = str(id['primary_ip4']['address'])
        else:
            primary_ip4 = 'null'
        manager_name = str(id['manager']['username'])
        manager_mail = str(id['manager']['email'])
        if id['switch'] != None:
            switch_id = str(id['switch']['id'])
        else:
            switch_id = 'null'
        if id['san_switch'] != None:
            san_switch_id = str(id['san_switch']['id'])
        else:
            san_switch_id = 'null'
        if id['storage'] != None:
            storage_id = str(id['storage']['id'])
        else:
            storage_id = 'null'
        if id['firewall'] != None:
            firewall_id = str(id['firewall']['id'])
        else:
            firewall_id = 'null'
        if id['load_balancer'] != None:
            load_balancer_id = str(id['load_balancer']['id'])
        else:
            load_balancer_id = 'null'
          
        # insert the data into the table
        data =     {'device_id': [device_id],
                    'device_name': [device_name],
                    'device_type': [device_type],
                    'device_type_manufacture': [device_type_manufacture],
                    'device_role': [device_role],
                    'serial': [serial],
                    'site': [site],
                    'location': [location],
                    'rack': [rack],
                    'status': [status],
                    'primary_ip4': [primary_ip4],
                    'manager_name': [manager_name],
                    'manager_mail': [manager_mail],
                    'switch_id': [ switch_id],
                    'san_switch_id': [san_switch_id],
                    'storage_id': [storage_id],
                    'firewall_id': [firewall_id],
                    'load_balancer_id': [load_balancer_id]}                       
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO Device (Device_ID, Device_name, Device_type, Device_type_manufacture, Device_role, Serial, Site, Location, Rack, Status, Primary_ip4, Manager_name, Manager_mail, Switch_ID, San_switch_ID, Storage_ID, Firewall_ID, Load_balancer_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE Device_name=%s, Device_type=%s, Device_type_manufacture=%s, Device_role=%s, Serial=%s, Site=%s, Location=%s, Rack=%s, Status=%s, Primary_ip4=%s, Manager_name=%s, Manager_mail=%s, Switch_ID=%s, San_switch_ID=%s, Storage_ID=%s, Firewall_ID=%s, Load_balancer_ID=%s"
            val = (row['device_id'], row['device_name'], row['device_type'], row['device_type_manufacture'], row['device_role'], row['serial'], row['site'], row['location'], row['rack'], row['status'], row['primary_ip4'], row['manager_name'], row['manager_mail'], row['switch_id'], row['san_switch_id'], row['storage_id'], row['firewall_id'], row['load_balancer_id'])
            cursor.execute(sql, val)
        
        # commit the changes to the database
        cnx.commit()

    offset = offset + 50                                       # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()

