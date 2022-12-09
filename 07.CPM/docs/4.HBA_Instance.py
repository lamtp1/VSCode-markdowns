from asyncio.windows_events import NULL
import asyncore
from re import S
import requests
import json
ip_url = "http://dcim.viettel.vn/api/ipam/ip-addresses/"
extra_url = "http://dcim.viettel.vn/api/dcim/dcim-extra-data/"

#temp_qr= {"assigned_to_interface":"True","limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token  bda193b23ccdb7eb6e341a87d36e72c564214165",
    'Cache-Control': "no-cache",
    }
#response = requests.request("GET", url, headers=headers, params=temp_qr)
#ip_count = response.json()['count']

#limit= 250
#offset= 0
hba_wwn = open("hba.txt", "w")
ipfile = open("hba_ip.txt", "r")
for ip in ipfile:
    qr_ip = {"address":ip}
    rp= requests.request("GET", ip_url, headers=headers, params=qr_ip).json()['results'][0]
    if rp['assigned_object'] !=None:
        if rp['assigned_object']['instance'] != None:
            as_name = rp['assigned_object']['instance']['id']
            # as_name la gi? ma can mang 3 chieu
    else:
        as_name= None

    if as_name != None:
        qr_hba= {"instance_id":as_name}
        rp_hba= requests.request("GET", extra_url , headers=headers, params=qr_hba).json()['results'][0]
        hba_p1=str(rp_hba['metadata_info']['HBA']['rows'][0]['port_name'])
        hba_p2=str(rp_hba['metadata_info']['HBA']['rows'][1]['port_name'])
    else:
        hba_p1='blank'
        hba_p1='blank'
    
    print (ip.strip() + ' ' + hba_p1 + ' ' + hba_p2 )
    s = ip.strip() + ' ' + hba_p1 + ' ' + hba_p2 +'\n'
    hba_wwn.write(s)
hba_wwn.close()
ipfile.close()