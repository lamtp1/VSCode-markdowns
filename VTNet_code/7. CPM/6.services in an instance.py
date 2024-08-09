import requests
import json

url = "http://dcim.viettel.vn/api/service/services/"

querystring = {"instance_id":"26038"}

headers = {
    'Content-Type': "application/json",
    'Authorization': "Token bda193b23ccdb7eb6e341a87d36e72c564214165",
    'Cache-Control': "no-cache",
    }

response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)

lines =  response.text

# in ra ket qua vao file text
with open('services in an instance.txt', 'w', encoding="utf-8") as f:
    f.write(lines)

# in ra ket qua dang json tren terminal
with open('services in an instance.txt', 'r') as read_file:
    object = json.load(read_file)
    pretty_object = json.dumps(object, indent=4)
    print(pretty_object)

# overwrite vao file dau tien
with open('services in an instance.txt', 'w', encoding="utf-8") as f:
    f.write(pretty_object)