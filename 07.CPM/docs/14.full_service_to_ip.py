import asyncore
import json
from asyncio.windows_events import NULL
from re import S

import requests

# lay ipv4 primary tu api instance
ip_url = 'http://dcim.viettel.vn/api/service/service-user/'
service_url = 'http://dcim.viettel.vn/api/service/service/'

temp_qr= {"limit":1}
headers = {
    'Content-Type': "application/json",
    'Authorization': "Token   babc4e664e88d033892f5f0240bd86664b5c9c48",
    'Cache-Control': "no-cache",
    }
# response = requests.request("GET", service_url, headers=headers, params=temp_qr)
# ip_count = response.json()['count']

limit= 5
offset= 0
service_file = open("service_code.txt", "r+", encoding='UTF-8')
while offset <= 20 :
    querystring = {"limit":limit, "offset": offset}
    response= requests.request("GET", service_url, headers=headers, params=querystring).json()['results']
    for code in response:
        if code['name'] != None:
            service_code = str(code['name'])
        else:
            service_code = None
        if  service_code == None:
            s = None
        else:
            s =  service_code + '\n'
            service_file.write(s)
        # print(ipaddr + '\n' )
    # ipfile.close()

# ghep file tu cho service_to_ip
    service_file = open("service_code.txt", "r+", encoding='UTF-8')
    w =  open('service_to_ip.txt', 'w', encoding='UTF-8')

    for code in service_file:  # do khong phai service_name nao cx co service_code => tim bang name se day du hon
        qr_code = {"name":code}
        rp= requests.request("GET", service_url, headers=headers, params=qr_code).json()['results']
        for i in rp:
            x =rp.index(i)
            if rp[x]['id'] !=None:
                service_id = rp[x]['id']
            else:
                service_id = None  # co hien thi gi tren man hinh khong?

            if service_id != None:
                service_id = {"service_id":service_id}
                rp2 = requests.request("GET", ip_url , headers=headers, params=service_id).json()['results']
                for id in rp2:
                    i=rp2.index(id) # moi id trong response se duoc danh index bat dau tu 0
                    rp2i = rp2[i]
                    ip = str(rp2i['instance']['name'])
                    print (code.strip() + ' '+ ip + '\n')
                    s = code.strip() + ' '+ ip + '\n'
                    w.write(s)
            else:
                service = None
    offset = offset + 5
w.close()
service_file.close()