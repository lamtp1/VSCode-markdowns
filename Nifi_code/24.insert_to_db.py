import asyncore
import json
from asyncio.windows_events import NULL
from re import S
import pandas as pd
import openpyxl
import requests
import mysql.connector


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
table_name = 'Device_test_2'

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

        # insert the data into the table
        data =     {'device_id': [device_id],
                    'device_name': [device_name],
                    'device_type': [device_type],
                    'device_type_manufacture': [device_type_manufacture],
                    'device_role': [device_role]
                    }                       
        df = pd.DataFrame(data)           
        # insert_query = f"INSERT INTO {table_name} (device_id, device_name, device_type, device_type_manufacture, device_role) VALUES (%s, %s, %s, %s, %s)"
        # for row in df.itertuples(index=False):
        #     cursor.execute(insert_query, row)
        
        # # commit the changes to the database
        # cnx.commit()

    offset = offset + 50                                       # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()

