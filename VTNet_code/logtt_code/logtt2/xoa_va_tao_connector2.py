import requests
import json
import urllib3
import ssl

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Duong dan den cac file chung chi
cert_path = './cert/client-cert.pem'
key_path = './cert/client-key.pem'
cacert_path = './cert/CA_cert.pem'

# Doc danh sach cac API tu file txt
api_file_path = "api_logtt2_connetor.txt"  # Thay doi duong dan neu can
with open(api_file_path, 'r') as file:
    api_urls = [line.strip() for line in file.readlines()]

results = []
error_connectors = []

# Kiem tra trang thai cua tung connector
for api_url in api_urls:
    try:
        # Gui yeu cau HTTP GET voi chung chi
        response = requests.get(api_url, cert=(cert_path, key_path), verify=False)
        response.raise_for_status()  # Kiem tra neu co loi HTTP
        data = response.json()  # Chuyen ket qua thanh dang JSON

        # Lay ten cua connector
        connector_name = data.get("name", "Unknown")
        system_name = connector_name.split('-')[2]  # Lay ten he thong, vi du: 'qlhs' tu 'es-centralizedlog-qlhs-connector'

        # Kiem tra trang thai cua tat ca cac tasks
        task_states = [task["state"] for task in data.get("tasks", [])]
        if "FAILED" in task_states:
            status = "Error"
            error_connectors.append(system_name)  # Them vao danh sach connector loi
#        else:
#            status = "Active"

        # Ghi ket qua vao danh sach
            results.append(f"{connector_name} | {status}")

    except requests.exceptions.RequestException as e:
        # Neu co loi khi gui yeu cau
        results.append(f"Error with API: {api_url} - {str(e)}")

# In ra ket qua
print("Ket qua check lan 1")
for result in results:
    print(result)

# Kiem tra xem co loi nao khong
if not any("Error" in result for result in results):
    print("everything is okay")
print("\n")
# Ghi ket qua vao file txt
#output_file_path = "connector_status_results.txt"
#with open(output_file_path, 'w') as file:
#    for result in results:
#        file.write(result + "\n")

# Ghi them dong "everything is okay" vao file neu khong co loi
#if not any("Error" in result for result in results):
#    with open(output_file_path, 'a') as file:
#        file.write("everything is okay\n")

# Xoa cac connector co loi
for system in error_connectors:
    delete_url = f"https://10.254.139.177:8083/connectors/es-centralizedlog-{system}-connector"
    try:
        delete_response = requests.delete(delete_url, cert=(cert_path, key_path), verify=False)
        delete_response.raise_for_status()  # Kiem tra neu co loi HTTP
        print(f"Deleted connector: es-centralizedlog-{system}-connector")
    except requests.exceptions.RequestException as e:
        print(f"Failed to delete connector: es-centralizedlog-{system}-connector - {str(e)}")

# Tao lai cac connector co loi
for system in error_connectors:
    create_url = f"https://10.254.139.180:8083/connectors/es-centralizedlog-{system}-connector/config"
    config_data = {
        "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
        "connection.url": "https://10.254.139.167:9200,https://10.254.139.167:9201,https://10.254.139.167:9202,https://10.254.139.167:9203,https://10.254.139.168:9200,https://10.254.139.168:9201,https://10.254.139.168:9202,https://10.254.139.168:9203,https://10.254.139.169:9200,https://10.254.139.169:9201,https://10.254.139.169:9202,https://10.254.139.169:9203,https://10.254.139.170:9200,https://10.254.139.170:9201,https://10.254.139.170:9202,https://10.254.139.170:9203,https://10.254.139.171:9200,https://10.254.139.171:9201,https://10.254.139.171:9202,https://10.254.139.171:9203,https://10.254.139.172:9200,https://10.254.139.172:9201,https://10.254.139.172:9202,https://10.254.139.172:9203,https://10.254.139.173:9200,https://10.254.139.173:9201,https://10.254.139.173:9202,https://10.254.139.173:9203,https://10.254.139.174:9200,https://10.254.139.174:9201,https://10.254.139.174:9202,https://10.254.139.174:9203,https://10.254.139.175:9200,https://10.254.139.175:9201,https://10.254.139.175:9202,https://10.254.139.175:9203,https://10.254.139.176:9200,https://10.254.139.176:9201,https://10.254.139.177:9200,https://10.254.139.177:9201,https://10.254.139.178:9200,https://10.254.139.178:9201,https://10.254.139.179:9200,https://10.254.139.179:9201,https://10.254.139.180:9200,https://10.254.139.180:9201,https://10.254.139.181:9200,https://10.254.139.182:9200",
        "connection.username": "kafka_connect",
        "connection.password": "Vtlog!@2022",
        "group.id": "connect-cluster",
        "topics": f"es.centralizedlog.{system.upper()}",
        "name": f"es-centralizedlog-{system}-connector",
        "value.converter": "org.apache.kafka.connect.json.JsonConverter",
        "value.converter.schemas.enable": "false",
        "key.ignore": "true",
        "schema.ignore": "true",
        "max.connection.idle.time.ms": "600000",
        "read.timeout.ms": "0",
        "flush.timeout.ms": "300000",
        "max.buffered.records": "1000000",
        "batch.size": "100000",
        "linger.ms": "100",
        "connection.timeout.ms": "10000",
        "errors.tolerance": "all",
        "errors.log.enable": "true",
        "errors.log.include.messages": "true",
        "behavior.on.malformed.documents": "warn",
        "tasks.max": "21",
        "flush.synchronously": "true",
        "transforms": "routeTS",
        "transforms.routeTS.type": "org.apache.kafka.connect.transforms.TimestampRouter",
        "transforms.routeTS.topic.format": "${{topic}}-${{timestamp}}",
        "transforms.routeTS.timestamp.format": "yyyy.MM",
        "elastic.security.protocol": "SSL",
        "elastic.https.ssl.keystore.location": "/etc/kafka-connect/secrets/es.client.keystore.jks",
        "elastic.https.ssl.keystore.password": "123123",
        "elastic.https.ssl.key.password": "123123",
        "elastic.https.ssl.keystore.type": "JKS",
        "elastic.https.ssl.truststore.location": "/etc/kafka-connect/secrets/es.client.truststore.jks",
        "elastic.https.ssl.truststore.password": "123123",
        "elastic.https.ssl.truststore.type": "JKS",
        "elastic.https.ssl.protocol": "TLS"
    }
    headers = {"Content-Type": "application/json"}
    try:
        create_response = requests.put(create_url, headers=headers, data=json.dumps(config_data), cert=(cert_path, key_path), verify=False)
        create_response.raise_for_status()  # Kiem tra neu co loi HTTP
        print(f"Created connector: es-centralizedlog-{system}-connector")
    except requests.exceptions.RequestException as e:
        print(f"Failed to create connector: es-centralizedlog-{system}-connector - {str(e)}")
print("\n")
# Kiem tra lai trang thai cua cac connector
results = []
for api_url in api_urls:
    try:
        response = requests.get(api_url, cert=(cert_path, key_path), verify=False)
        response.raise_for_status()
        data = response.json()
        connector_name = data.get("name", "Unknown")
        task_states = [task["state"] for task in data.get("tasks", [])]
        if "FAILED" in task_states:
            status = "Error"
#        else:
#            status = "Active"
            results.append(f"{connector_name} | {status}")
    except requests.exceptions.RequestException as e:
        results.append(f"Error with API: {api_url} - {str(e)}")

print("Ket qua check lan 2")
for result in results:
    print(result)
if not any("Error" in result for result in results):
    print("everything is okay")

