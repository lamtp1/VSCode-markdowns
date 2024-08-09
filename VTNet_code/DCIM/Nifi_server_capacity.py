import requests
import json
import asyncore
import pandas as pd
import mysql.connector
from datetime import datetime

capacity_url = 'http://10.255.58.203/api/dcim/instance-generals/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }

rp1 = requests.request("GET",capacity_url, headers=headers, params=temp_qr)
ip_count = rp1.json()['count']

cnx = mysql.connector.connect(user='root', password='123456',
                              host='10.254.139.183', port=3306, database='CPM')
cursor = cnx.cursor()

limit= 250
offset= 0
# capacity_file = open("capacity_file.txt", "w+", encoding = 'UTF-8')
while offset <  ip_count:
    qr_param = {"limit":limit, "offset": offset}
    rp2 = requests.request("GET", capacity_url , headers=headers, params=qr_param).json()['results']
    for id in rp2:
        # lay thong tin module (service_user_id va module_id,code,name,group code,name)
        if id['general'] != None:
            Instance_ID = str(id['instance'])
            Memtotal_mb = str(id["general"]["rows"][0].get('memtotal_mb', None))
            Processor_vcpus = str(id["general"]["rows"][0].get('processor_vcpus', None))

            s = Instance_ID + "|" + Memtotal_mb + "|" + Processor_vcpus + "\n"
            # capacity_file.write(s)
        else:
            Instance_ID = str(id['instance'])
            Memtotal_mb = None
            Processor_vcpus = None

            # s = instance + "|" + memtotal_mb + "|" + processor_vcpus + "\n"
            # capacity_file.write(s)
        # lay thong tin username va instance_id tu api service-users 

        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data =  {'Instance_ID': [Instance_ID],
                'Memtotal_mb': [Memtotal_mb],
                'Processor_vcpus': [Processor_vcpus],
                'insert_time': [insert_time]}
                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO Server_capacity (Instance_ID, Processor_vcpus, Memtotal_mb, insert_time) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE  Processor_vcpus=%s, Memtotal_mb=%s"
            val = (row['Instance_ID'], row['Processor_vcpus'], row['Memtotal_mb'], insert_time, row['Processor_vcpus'], row['Memtotal_mb'])
            cursor.execute(sql, val)
        # df_string = df.to_string(index=False)
        # print(df_string)

        # commit the changes to the database
        cnx.commit()

    offset = offset + 250                                       # de offset ngoai vong for se bi lap 3 lan => de offset ben trong

# close the cursor and database connection
cursor.close()
cnx.close()
# capacity_file.close()
print('success')