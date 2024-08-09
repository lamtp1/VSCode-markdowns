from asyncio.windows_events import NULL
import asyncore
from re import S
import requests
import json
url = "http://dcim.viettel.vn/api/ipam/ip-addresses/"

temp_qr= {"status":"active","assigned_to_interface":"False","limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token   babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }
response = requests.request("GET", url, headers=headers, params=temp_qr)
ip_count = response.json()['count']

limit= 250
offset= 0
ipfile = open("status_dcim.txt", "w")
while offset < 5000 :
    querystring = {"status":"active","assigned_to_interface":"False","limit":limit, "offset": offset}
    response= requests.request("GET", url, headers=headers, params=querystring).json()['results']
    for ip in response:
        ipaddr = str(ip['address'])
        id_ip = str(ip['id'])
        s = ipaddr+ '\n'
        ipfile.write(s)
        # print(ipaddr + '\n' )
    offset = offset + 250
ipfile.close()
