import asyncore
import json
from re import S
import pandas as pd
import requests
import mysql.connector
from datetime import datetime
from requests.exceptions import ConnectTimeout
import time

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
# cnx = mysql.connector.connect(user='root', password='123456',
#                               host='10.254.139.183', port=3306, database='Netbi')
# cursor = cnx.cursor()

limit= 250
offset= 0
Device_file = open('Device_file.txt', 'w+', encoding = 'UTF-8')
while offset <  ip_count:
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
            primary_ip4 = str(id['primary_ip4']['address'].split('/',1)[0])
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
            firewall_id = str(id['firewall'])
        else:
            firewall_id = 'null'
        if id['load_balancer'] != None:
            load_balancer_id = str(id['load_balancer']['id'])
        else:
            load_balancer_id = 'null'
        created = str(id['created'])
        if id['tenant'] != None:
            tenant = str(id['tenant']['name'])
        else:
            tenant = 'null'
            
        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        s = device_id + '|' + device_name + '|' + device_type + '|' + device_type_manufacture + '|' + device_role + '|' + serial + '|' + site + '|' + location + '|' + rack + '|' + status + '|' + primary_ip4 + '|' + manager_name + '|' + manager_mail + '|' + switch_id + '|' + san_switch_id + '|' + storage_id + '|' + firewall_id + '|' + load_balancer_id + '|' + created + '|' + tenant + '|' + insert_time + '\n'

        Device_file.write(s)

        # insert the data into the table
        # data =     {'Device_ID': [device_id],
        #             'Device_name': [device_name],
        #             'Device_type': [device_type],
        #             'Device_type_manufacture': [device_type_manufacture],
        #             'Device_role': [device_role],
        #             'Serial': [serial],
        #             'Site': [site],
        #             'Location': [location],
        #             'Rack': [rack],
        #             'Status': [status],
        #             'Primary_ip4': [primary_ip4],
        #             'Manager_name': [manager_name],
        #             'Manager_mail': [manager_mail],
        #             'Switch_ID': [ switch_id],
        #             'San_switch_ID': [san_switch_id],
        #             'Storage_ID': [storage_id],
        #             'Firewall_ID': [firewall_id],
        #             'Load_balancer_ID': [load_balancer_id],
        #             'created': [created],
        #             'tenant': [tenant],
        #             'insert_time': [insert_time]}                       
        # df = pd.DataFrame(data)           
        # for index, row in df.iterrows():
        #     sql = "INSERT INTO Device (Device_ID, Device_name, Device_type, Device_type_manufacture, Device_role, Serial, Site, Location, Rack, Status, Primary_ip4, Manager_name, Manager_mail, Switch_ID, San_switch_ID, Storage_ID, Firewall_ID, Load_balancer_ID, created, tenant, insert_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE Device_name=%s, Device_type=%s, Device_type_manufacture=%s, Device_role=%s, Serial=%s, Site=%s, Location=%s, Rack=%s, Status=%s, Primary_ip4=%s, Manager_name=%s, Manager_mail=%s, Switch_ID=%s, San_switch_ID=%s, Storage_ID=%s, Firewall_ID=%s, Load_balancer_ID=%s"
        #     val = (row['Device_ID'], row['Device_name'], row['Device_type'], row['Device_type_manufacture'], row['Device_role'], row['Serial'], row['Site'], row['Location'], row['Rack'], row['Status'], row['Primary_ip4'], row['Manager_name'], row['Manager_mail'], row['Switch_ID'], row['San_switch_ID'], row['Storage_ID'], row['Firewall_ID'], row['Load_balancer_ID'],  row['created'], row['tenant'], insert_time, row['Device_name'], row['Device_type'], row['Device_type_manufacture'], row['Device_role'], row['Serial'], row['Site'], row['Location'], row['Rack'], row['Status'], row['Primary_ip4'], row['Manager_name'], row['Manager_mail'], row['Switch_ID'], row['San_switch_ID'], row['Storage_ID'], row['Firewall_ID'], row['Load_balancer_ID'])
        #     cursor.execute(sql, val)
        
        # df_string = df.to_string(index=False)
        # print(df_string)
        # commit the changes to the database
        # cnx.commit()

    offset = offset + 250                                       # de offset ngoai vong for se bi lap 3 lan => de offset ben trong
    # time.sleep(30)

# close the cursor and database connection
# cursor.close()
# cnx.close()
print('success')