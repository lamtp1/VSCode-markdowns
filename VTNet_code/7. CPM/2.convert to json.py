import requests
import json

url = "http://dcim.viettel.vn/api/service/service-users/"

querystring = {"service_id":"504"}

headers = {
    'Content-Type': "application/json",
    'Authorization': "Token   b1e04e3e48706fa80132baa3753336de382a9f25",
    'Cache-Control': "no-cache",
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text) 

lines =  response.text

#in ket qua ra file text:
with open('instances in an service.txt', 'w', encoding='UTF-8') as w:
    w.write(lines)

#in ket qua dang json ra terminal:
with open('instances in an service.txt', 'r') as read_file:
    object = json.load(read_file)
    pretty_object = json.dumps(object, indent=4)
    print(pretty_object)

#overwrite ket qua vao file text dau tien:
with open('instances in an service.txt', 'w', encoding='UTF-8') as w:
    w.write(pretty_object)


