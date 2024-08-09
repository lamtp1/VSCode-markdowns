import requests
import json
import urllib3
import ssl

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Doc danh sach API tu file txt
api_file_path = "list_connectors.txt"  
with open(api_file_path, 'r') as file:
    api_urls = [line.strip() for line in file.readlines()]

results = []
error_connectors = []

# Kiem tra trang thai cua tung connector
for api_url in api_urls:
    try:
        # Gui yeu cau HTTP GET
        response = requests.get(api_url, verify=False)
        response.raise_for_status()  # Kiem tra neu co loi HTTP
        data = response.json()  # Chyen ket qua  thành dạng JSON

        # Lay ten cua connector
        connector_name = data.get("name", "Unknown")
        system_name = connector_name.split('-')[2]  # Lay ten he thong, ví dụ: 'qlhs' từ 'es-centralizedlog-qlhs-connector'

        # Kiem tra trang thai cua tat ca cac tasks
        task_states = [task["state"] for task in data.get("tasks", [])]
        if "FAILED" in task_states:
            status = "Error"
            error_connectors.append(system_name)  # Them vao danh sach connector loi
        #else:
        #    status = "Active"

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

# Xoa cac connector co loi
for system in error_connectors:
    delete_url = f"http://10.254.138.3:8083/connectors/es-centralizedlog-{system}-connector"
    try:
        delete_response = requests.delete(delete_url, verify=False)
        delete_response.raise_for_status()  # Kiem tra neu co loi HTTP
        print(f"Deleted connector: es-centralizedlog-{system}-connector")
    except requests.exceptions.RequestException as e:
        print(f"Failed to delete connector: es-centralizedlog-{system}-connector - {str(e)}")
print("\n")

# Tao lai cac connector co loi
for system in error_connectors:
    create_url = f"http://10.254.138.10:8083/connectors/es-centralizedlog-{system}-connector/config"
    config_data = {
        "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
        "connection.url": "https://10.254.138.3:9200,https://10.254.138.4:9200,https://10.254.138.5:9200,https://10.254.138.5:9201,https://10.254.138.6:9200,https://10.254.138.6:9201,https://10.254.138.7:9200,https://10.254.138.7:9201,https://10.254.138.10:9200",
        "connection.username": "kafka_connect",
        "connection.password": "Vtlog!@2022",
        "group.id": "connect-cluster",
        "topics": f"es.centralizedlog.{system.upper()}",
        "name": f"es-centralizedlog-{system}-connector",
        "type.name": "_doc",
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
        "transforms": "routeTS",
        "transforms.routeTS.type": "org.apache.kafka.connect.transforms.TimestampRouter",
        "transforms.routeTS.topic.format": "${topic}-${timestamp}",
        "transforms.routeTS.timestamp.format": "yyyy.MM",
        "elastic.security.protocol": "SSL",
        "elastic.https.ssl.keystore.location": "/usr/share/kafka-connect/config/keystore.jks",
        "elastic.https.ssl.keystore.password": "123123",
        "elastic.https.ssl.key.password": "123123",
        "elastic.https.ssl.keystore.type": "JKS",
        "elastic.https.ssl.truststore.location": "/usr/share/kafka-connect/config/truststore.jks",
        "elastic.https.ssl.truststore.password": "123123",
        "elastic.https.ssl.truststore.type": "JKS",
        "elastic.https.ssl.protocol": "TLS"
    }
    headers = {"Content-Type": "application/json"}
    try:
        create_response = requests.put(create_url, headers=headers, data=json.dumps(config_data), verify=False)
        create_response.raise_for_status()  # Kiem tra neu co loi HTTP
        print(f"Created connector: es-centralizedlog-{system}-connector")
    except requests.exceptions.RequestException as e:
        print(f"Failed to create connector: es-centralizedlog-{system}-connector - {str(e)}")
print("\n")

# Kiem tra lai trang thai cua cac connector
results = []
for api_url in api_urls:
    try:
        response = requests.get(api_url, verify=False)
        response.raise_for_status()
        data = response.json()
        connector_name = data.get("name", "Unknown")
        task_states = [task["state"] for task in data.get("tasks", [])]
        if "FAILED" in task_states:
            status = "Error"
        #else:
        #     status = "Active"
            results.append(f"{connector_name} | {status}")
    except requests.exceptions.RequestException as e:
        results.append(f"Error with API: {api_url} - {str(e)}")

print("Ket qua kiem tra lan 2")
for result in results:
    print(result)

if not any("Error" in result for result in results):
    print("everything is okay")

