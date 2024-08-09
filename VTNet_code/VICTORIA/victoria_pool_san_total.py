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

url = "http://10.254.139.73:8501/api/v1/query"
usr="npms"
pas="Npms@123"

headers = {
    'Content-Type': "application/json",
    'Content-Encoding': "gzip",
    'Cache-Control': "no-cache",
    }

cnx = mysql.connector.connect(user='root', password='123456',
                              host='10.254.139.183', port=3306, database='CPM')
cursor = cnx.cursor()

# ouputfile = open("total_pool_san.txt", "w", encoding="utf-8")
pool_qr= 'san_pool_total_capacity_mib'
payload = {'query': pool_qr}
rq=requests.request("GET", url, headers=headers, auth=(usr, pas), params=payload).json()["data"]["result"]
# cmt="Pool Name|SAN IP|Capacity|IP check\n"
# ouputfile.write(cmt)
for i in rq:
        pool_name=i["metric"]["pool_name"]
        san_ip=i["metric"]["san_ip"]
        value=i["value"][1]
        values=float(value)/1024
        a=san_ip.split('.',3)[0]
        b=san_ip.split('.',3)[1]
        c=san_ip.split('.',3)[2]
        d=san_ip.split('.',3)[3]
        ip_check = str(a)+str(b)+str(c)+str(d)
        insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data =  {'pool_name': [pool_name],
                'san_ip': [san_ip],
                'capacity': [values],
                'ip_check': [ip_check],
                'insert_time': [insert_time]}                
        df = pd.DataFrame(data)           
        for index, row in df.iterrows():
            sql = "INSERT INTO victoria_pool_san_total (pool_name, san_ip, capacity, ip_check, insert_time) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE  pool_name=%s, san_ip=%s, capacity=%s, ip_check=%s, insert_time=%s"
            val = (row['pool_name'], row['san_ip'], row['capacity'], row['ip_check'], insert_time, row['pool_name'], row['san_ip'], row['capacity'], row['ip_check'], insert_time)
            cursor.execute(sql, val)

        cnx.commit()

cursor.close()
cnx.close()
print('success')        
        # if len(c)<3:
        #     c1=str(0)+str(c)
        #     s= str(pool_name) + "|" + str(san_ip) + "|"  + str(values) + "|"  + ip_check + "\n"
        # else:
        #     s= str(pool_name) + "|" + str(san_ip) + "|"  + str(values) + "|"  + ip_check + "\n"
        #   print(str(a)+str(b)+str(c1)+str(d))
        
        # ouputfile.write(s)
            # print(s)
# ouputfile.close()

