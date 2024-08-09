import requests
import json
import urllib3
import ssl

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ssl.match_hostname = lambda cert, hostname: False

# Duong dan den file cert, key va cacert
cert_path = "./cert/client-cert.pem"
key_path = "./cert/client-key.pem"
cacert_path = "./cert/CA_cert.pem"

# Doc danh sach API tu file text
api_file_path = "api_logtt2_connetor.txt"  # file chua API
with open(api_file_path, 'r') as file:
    api_urls = [line.strip() for line in file.readlines()]

results = []

# Cau hinh client cert va client key
cert = (cert_path, key_path)

# Kiem tra trang thai cua tung connecotr
for api_url in api_urls:
    try:
        response = requests.get(api_url, cert=cert, verify=False)  # Goi request HTTP GET
        response.raise_for_status()  # Kiem tra neu co loi http
        data = response.json()  # Chuyen ket qua thanh dang json

        # Lay ten cua connector
        connector_name = data.get("name", "Unknown")

        # Kiem tra trang thai cua tat ca cac task
        task_states = [task["state"] for task in data.get("tasks", [])]
        if "FAILED" in task_states:
            status = "Error"  # Neu co bat ky taask nao failed
       # else:
       #     status = "Active"  # Neu tat ca cac task deu chay

        # Ghi ket qua vao list
            results.append(f"{connector_name} | {status}")

    except requests.exceptions.RequestException as e:
        # thong bao neu co loi khi gui request
        results.append(f"Error with API: {api_url} - {str(e)}")

# In ra man hinh
for result in results:
    print(result)

if not any("Error" in result for result in results):
    print("Moi chuyen deu on, khong phai lo!")

# Ghi ket qua vao file text
#output_file_path = "connector_status_results.txt"  # PATH file text
#with open(output_file_path, 'w') as file:
#    for result in results:
#        file.write(result + "\n")

