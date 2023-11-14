import requests
import json
import asyncore
from asyncio.windows_events import NULL
import pandas as pd
import openpyxl

service_url = 'http://dcim.viettel.vn/api/service/service/'
owner_url = 'http://dcim.viettel.vn/api/service/service-managers/'
module_url = 'http://dcim.viettel.vn/api/service/modules/'
instance_url = 'http://dcim.viettel.vn/api/service/service-users/'

headers = {
    'Content-Type': "application/json",
    'Authorization': "Token    7e4ed69be74cfd475a1c361002b15b0169420f08",
    'Cache-Control': "no-cache",
    }

service_file = open("service_code.txt", "r")
w =  open('service_to_ip.txt', 'w', encoding='UTF-8')
for code in service_file:
    # lay thong tin service_id tu api service
    qr_code = {"code":code}
    rp= requests.request("GET", service_url, headers=headers, params=qr_code).json()['results'][0]
    if rp['id'] !=None:
        service_id = str(rp['id'])
    else:
        service_id = None  # co hien thi gi tren man hinh khong?

    if service_id != None:
        # lay thong tin service_manager va manager id tu api service_manager
        qr_param2 = {"service_id":service_id}
        rp3 = requests.request("GET", owner_url , headers=headers, params=qr_param2).json()
        if rp3['count'] != 0:
            service_manager = str(rp3["results"][0]["manager"]["username"])
            manager_id = str(rp3["results"][0]["manager"]["id"])
        else:
            service_owner = 'Không có user'
        
        count = requests.request("GET", module_url , headers=headers, params=service_id).json()['count']
        offset = 0
        limit = count
        while offset < count:
            qr_param = {"service_id":service_id, "limit":limit, "offset": offset}
            rp2 = requests.request("GET", module_url , headers=headers, params=qr_param).json()['results']
            for id in rp2:
                # lay thong tin module (service_user_id va module_id,code,name,group code,name)
                service_user_id = str(id['service_user']['id'])
                module_id = str(id['id'])
                if id['group'] != None:
                    group_code = str(id['group']['code'])
                    group_name = str(id['group']['name'])
                else:
                    group_code = 'Không có group code'
                    group_name = 'Không có group name'
                module_name = str(id['name'])
                module_code = str(id['code'])
                module_instance = str(id['service_user']['display_name'])

                # lay thong tin username va instance_id tu api service-users 
                rp4 = requests.request("GET", instance_url+service_user_id , headers=headers).json()
                instance_id = str(rp4['instance']['id'])
                username = str(rp4['username'])

                data =  {'service_code': [code],
                'service_id': [service_id],
                'service_manager': [service_manager],
                'manager_id': [manager_id],
                'module_code': [module_code],
                'module_name': [module_name],
                'module_instance': [module_instance],
                'module_id': [module_id],
                'group_code': [group_code],
                'group_name': [group_name],
                'instance_id': [instance_id],
                'service_user_id': [service_user_id],
                'username': [username]}                       
                df = pd.DataFrame(data)           
                try:
                    existing_df = pd.read_csv("thong_tin_instance.csv")
                    df = pd.concat([existing_df, df], ignore_index=True)
                except FileNotFoundError:
                    pass
                df.to_csv("thong_tin_module.csv", index=False) 

                # print ( code.strip() + '*'+ service_id + '*'  + service_manager + '*'+ manager_id + '*' + module_code + '*'+ module_name+ '*' + module_instance + '*'+ module_id+ '*'+ group_code+'*'+group_name+'*' + instance_id+ '*'+ service_user_id+ '*' + username + '\n')
                # s =  code.strip() + '*'+ service_id + '*'  + service_manager + '*' + manager_id + '*' + module_code + '*'+ module_name+ '*' + module_instance + '*'+ module_id+ '*'+ group_code+'*'+group_name+'*' + instance_id+ '*'+ service_user_id+ '*'+ username +'\n'
                # w.write(s)
                
            offset = offset + count
    else:
        service = None

w.close()
service_file.close()