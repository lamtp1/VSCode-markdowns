from asyncio.windows_events import NULL
import asyncore
from re import S
import requests
import json
url = "http://dcim.viettel.vn/api/dcim/dcim-extra-data/"

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token  bda193b23ccdb7eb6e341a87d36e72c564214165",
    'Cache-Control': "no-cache",
    }
response = requests.request("GET", url, headers=headers, params=temp_qr)
ip_count = response.json()['count']

limit= 150
offset= 0
ipfile = open("ram-cpu.txt", "w")
while offset < 100 :
    querystring = {"limit":limit, "offset": offset}
    response= requests.request("GET", url, headers=headers, params=querystring).json()['results']
    for id in response:
        i=response.index(id)
        rp = response[i]['metadata_info']['GENERAL']['rows'][0]
        if rp['virtualization_role'] == 'host':
            ram= rp['memtotal_mb']
            cpu = rp['processor_vcpus']
            print(str(ram) + '   ' + str(cpu))
    offset = offset + 150

