import requests
import json
import asyncore
import pandas as pd
import mysql.connector
from datetime import datetime
import time

drive_url = 'http://dcim.viettel.vn/api/dcim/instance-extra-data/'

limit_qr = {"limit": 1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
}

rp = requests.request("GET", drive_url, headers=headers, params=limit_qr)
ip_count = rp.json()['count']

limit = 250
offset = 0
drive_file = open("drive_file_limit.txt", "w+", encoding='UTF-8')

while offset < ip_count:
    rp1_param = {"limit": limit, "offset": offset}
    rp1 = requests.request("GET", drive_url, headers=headers,
                           params=rp1_param).json()['results']
    for id in rp1:
        # dùng try pass vì một số Instance không có key MOUNT_POINT
        Instance_ID = str(id['instance'])
        try:
            rows = id['metadata_info']['MOUNT_POINT']['rows']
        except KeyError:
            pass
        total_size = 0.0
        for row in rows:
            # dùng try pass để không bị lỗi KeyError do trên DCIM một số MOUNT_POINT ko có size_total
            try:
                row['size_total']
                if row['size_total'] != None and row['size_total'] != 'N/A' and row['size_total'].split()[1] != 'MiB':
                    if  row['size_total'].split()[1] == 'TiB':
                        size_total_str = float(row['size_total'].split()[0]) * 1024
                    else:
                        size_total_str = float(row['size_total'].split()[0])
                    total_size += round(size_total_str, 2)
            except KeyError:
                pass
        s = Instance_ID + "|" + str(total_size) + "|" + "\n"
        drive_file.write(s)

    offset = offset + 250
drive_file.close()
print('success')
