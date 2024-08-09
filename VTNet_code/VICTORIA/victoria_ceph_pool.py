import asyncore
from operator import is_not
from queue import Empty
from re import I, S, search
import requests
import json
from datetime import datetime
import time
import calendar
import re
import pandas as pd
import mysql.connector

url_1 = "http://10.254.139.73:8501/api/v1/query?query=%28ceph_pool_stored%7Bpool_id%3D~%22.%2A%22%7D%20%2B%20ceph_pool_max_avail%7Bpool_id%3D~%22.%2A%22%7D%29"
url_2 = "http://10.254.139.73:8501/api/v1/query"
usr="npms"
pas="Npms@123"

headers = {
    'Content-Type': "application/json",
    'Content-Encoding': "gzip",
    'Cache-Control': "no-cache",
    }

# cnx = mysql.connector.connect(user='root', password='123456',
#                               host='10.254.139.183', port=3306, database='CPM')
# cursor = cnx.cursor()

hafile = open("victoria_ceph.txt", "w", encoding = 'UTF-8')
header_hafile="Cum_Cloud|pool_id|total|used \n"
hafile.write(header_hafile)

ha_qr= 'ceph_pool_stored{pool_id=~".*"}'
payload = {'query': ha_qr}
rq=requests.request("GET", url_1, headers=headers, auth=(usr, pas)).json()["data"]["result"]
rq2=requests.request("GET", url_2, headers=headers, auth=(usr, pas), params=payload).json()["data"]["result"]

for i in rq:
    if str(i["metric"]["monitor"]) != "openstack-hlct5":
        Cum_Cloud=i["metric"]["monitor"]
        pool_id=i["metric"]["pool_id"]
        total=i["value"][1]

        # Tìm giá trị used tương ứng với Cum_Cloud và pool_id trong rq2
        used = None
        for j in rq2:
            if j["metric"]["monitor"] == Cum_Cloud and j["metric"]["pool_id"] == pool_id:
                used = j["value"][1]
                break
        
        if used is not None:
            insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            s = str(Cum_Cloud) + "|" + str(pool_id) + "|" + str(total) + "|" + str(used) + "|" + "\n"
            hafile.write(s)

        data =  {'Cum_Cloud': [Cum_Cloud],
                'pool_id': [pool_id],
                'total': [total],
                'used': [used],
                'insert_time': [insert_time]}                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO victoria_ceph (Cum_Cloud, pool_id, total, used, insert_time) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE  Cum_Cloud=%s, pool_id=%s, total=%s, used=%s, insert_time=%s"
            val = (row['Cum_Cloud'], row['pool_id'], row['total'], row['used'], insert_time, row['Cum_Cloud'], row['pool_id'], row['total'], row['used'], insert_time)
#             cursor.execute(sql, val)

#         cnx.commit()

# cursor.close()
# cnx.close()
print('success')


