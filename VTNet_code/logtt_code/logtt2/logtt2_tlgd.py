import requests
import numpy as np

# Danh sach cac API
api_urls = [
    "http://10.254.139.176:21111",
    "http://10.254.139.177:21111",
    "http://10.254.139.178:21111",
    "http://10.254.139.179:21111",
    "http://10.254.139.180:21111",
    "http://10.254.139.181:21111",
    "http://10.254.139.182:21111"
    # Them cac API khac tai day
]

# Danh sach (array) de luu tru cac gia tri consumerlags va logendoffset
consumerlags = []
logendoffsets = []

# Lay du lieu tu tat ca API
for url in api_urls:
    response = requests.get(url)
    if response.status_code == 200:
        # Chuyen response sang dang text va tach cac dong tu response ra cac dong don le, co tu khoa consumerlag va logendoffset
        lines = response.text.split("\n")   # coi nhu response ban dau la mot chuoi dai, ngan cach boi dau xuong dong (\n)
        for line in lines:
            if line.startswith("kafka_server_fetcherlagmetrics_consumerlag"):
                # Trich xuat gia tri consumerlag tu moi dong, moi dong co 2 phan: key va value, phan cach nhau boi dau " ", phan 2 (part[1]) la value
                parts = line.split(" ")
                # kiem tra do dai moi dong xem = 2 khong (du key va value) thi moi lam tiep
                if len(parts) == 2:
                    value = float(parts[1])
                    consumerlags.append(value)  # ghi them gia tri vao danh sach (array) consumerlags khai luc dau
            elif line.startswith("kafka_log_log_logendoffset"):
                # Trich xuat gia tri logendoffset
                parts = line.split(" ")
                if len(parts) == 2:
                    value = float(parts[1])
                    logendoffsets.append(value) 

# Tinh 95th percentile cho consumerlag va logendoffset
consumerlag_95th = np.percentile(consumerlags, 95)
logendoffset_95th = np.percentile(logendoffsets, 95)

# Tinh TLGD
if logendoffset_95th != 0:
    TLGD = (1 - (consumerlag_95th / logendoffset_95th)) * 100
else:
    TLGD = None  # Tranh chia cho 0

print("95th percentile cua consumerlag:", consumerlag_95th)
print("95th percentile cua logendoffset:", logendoffset_95th)
if TLGD is not None:
    print("Ti le giao dich (TLGD): {:.2f}%".format(TLGD))
else:
    print("Khong tinh duoc TLGD do logendoffset 95th percentile la 0")

