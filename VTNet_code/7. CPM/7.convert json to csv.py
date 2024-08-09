import requests
import json
import pandas as pd

# url = "http://dcim.viettel.vn/api/service/service-users/"

# querystring = {"service_id":"504"}

# headers = {
#     'Content-Type': "application/json",
#     'Authorization': "Token  6ed3f0a46f40e7207d88bf21a52159255a9b1424",
#     'Cache-Control': "no-cache",
#     }

# response = requests.request("GET", url, headers=headers, params=querystring)

# with open('json_to_csv.json', 'wb') as output:
#     output.write(response.content)

with open ('json_to_csv.json', encoding='utf-8') as inputfile:
    df = pd.read_json(inputfile)
df.to_csv('csvfile.csv', encoding='utf-8', index=False)