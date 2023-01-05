import asyncore
import json
from asyncio.windows_events import NULL
from re import S

import requests

# lay ipv4 primary tu api instance
url = "http://dcim.viettel.vn/api/dcim/instances/"
service_url = 'http://dcim.viettel.vn/api/service/services/'
ipam_url = 'http://dcim.viettel.vn/api/ipam/ip-addresses/'

temp_qr= {"limit":1}
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
while offset < 1000 :
    querystring = {"limit":limit, "offset": offset}
    response= requests.request("GET", url, headers=headers, params=querystring).json()['results']
    for ip in response:
        if ip['primary_ip4'] != None:
            if ip['primary_ip4']['address'] != None:
                ipaddr = str(ip['primary_ip4']['address'])
        else:
            ipaddr = None
        if ipaddr == None:
            s = None
        else:
            s = ipaddr + '\n'
            ipfile.write(s)
        # print(ipaddr + '\n' )
    offset = offset + 250
ipfile.close()

# ghep file tu cho ip_to_service
ipfile = open(r"C:\Users\lamtp1\Desktop\VSCode markdowns\7. CPM\status_dcim.txt", "r")
w =  open(r"C:\Users\lamtp1\Desktop\VSCode markdowns\7. CPM\instances_id.txt", "w", encoding="UTF-8")
w2 = open(r"C:\Users\lamtp1\Desktop\VSCode markdowns\7. CPM\ip_to_service.txt", "w", encoding="UTF-8")
for ip in ipfile:
    qr_ip = {"address":ip}
    rp= requests.request("GET", ipam_url, headers=headers, params=qr_ip).json()['results'][0]  # moi ip chi co mot id nen dung results[0] duoc
    if rp['assigned_object'] !=None:
        if rp['assigned_object']['instance'] != None:
            as_name = rp['assigned_object']['instance']['id']
            
    else:
        as_name= None  # bang None thi hien gi tren man hinh?
    # print (as_name)

    # in instance id ra file text de lam dau vao lay service id
    w.write(str(as_name)+"\n")

    if as_name != None:
        instance_id = {"instance_id":as_name}
        rp2 = requests.request("GET", service_url , headers=headers, params=instance_id).json()['results']
        for id in rp2:
            i=rp2.index(id) # moi id trong response se duoc danh index bat dau tu 0
            rp2i = rp2[i]
            service = str(rp2i['name'])
            # print (ip.strip() + ' ' + service)
            s = ip.strip() + ' ' + service + '\n'
            w2.write(s)
    else:
        service = None
w.close()
w2.close()
ipfile.close() 
