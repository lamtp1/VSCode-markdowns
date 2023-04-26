import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
host="192.168.209.144",
user="root",
password="160299",
database="cpm",
port=3306
)

# Create a cursor object
cursor = conn.cursor()

""" 
Viết câu query để lấy ra giá trị lớn nhất của food theo thời gian, điều kiện là thời gian = thời gian hiện tại, nếu muốn lấy giá trị max
của ngày trước đó, thì dùng DATE(fh.food_time) = CURDATE()-1. Sau đó group by name, ở đây name là food_name, tương tự với LB,FW, group by
sẽ là ID hoặc name của LB, FW.

Muốn câu query này chạy thì BẮT BUỘC bảng hour phải đủ ít nhất đủ 24 dữ liệu trong ngày. Vậy nên tần suất chạy bảng này trên Nifi là
1 lần/ngày. Chạy cùng lúc với bảng hour hoặc sau một vài phút.
"""
query = "SELECT food_name, MAX(food_value) AS GTLN, food_time, food_id FROM food_hour fh WHERE DATE(fh.food_time) = CURDATE()+1 GROUP BY food_name"
cursor.execute(query)

# Fetch the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Insert the results into the 'food_day' table
insert_query = "INSERT INTO food_day (name, value, time, id) VALUES (%s, %s, %s, %s)"
for row in results:
    cursor.execute(insert_query, row)

# Commit the changes to the database
conn.commit()

# Close the cursor and the database connection
cursor.close()
conn.close()