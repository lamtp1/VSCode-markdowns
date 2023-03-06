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
cnx = mysql.connector.connect(user='root', password='160299',
                              host='192.168.209.144', port=3306, database='cpm')
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

        # insert the data into the table
        data =     {'device_id': [device_id],
                    'device_name': [device_name],
                    'device_type': [device_type],
                    'device_type_manufacture': [device_type_manufacture],
                    'device_role': [device_role]
                    }                       
        df = pd.DataFrame(data)     

        # df_string = df.to_string(index=False)
        # print(df_string)

        # loop through each row in the DataFrame and insert/update the MySQL table accordingly, data=val
        for index, row in df.iterrows():
            sql = "INSERT INTO device (device_id, device_name, device_type, device_type_manufacture, device_role) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE device_name = %s, device_type = %s, device_type_manufacture = %s, device_role = %s"
            val = (row['device_id'], row['device_name'], row['device_type'], row['device_type_manufacture'], row['device_role'], row['device_name'], row['device_type'], row['device_type_manufacture'], row['device_role'])
            cursor.execute(sql, val)
        
        # commit the changes to the database
        cnx.commit()

    offset = offset + 50                                       # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()

