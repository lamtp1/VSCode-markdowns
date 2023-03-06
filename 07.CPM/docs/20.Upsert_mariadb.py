import mysql.connector
import pandas as pd

# create a connection to your MySQL database
conn = mysql.connector.connect(
    host='192.168.209.144',
    user='root',
    password='160299',
    database='cpm',
    port=3306
)

# create a DataFrame with your data
data = {'id': [5, 9, 7],
        'name': ['Duynd21', 'Dungnd18', 'Anth79'], 
        'age': [40, 35, 41], 
        'gender': ['M', 'M', 'F']}
df = pd.DataFrame(data)

# create a cursor object to execute SQL statements
cursor = conn.cursor()

# loop through each row in the DataFrame and insert/update the MySQL table accordingly
for index, row in df.iterrows():
    sql = "INSERT INTO people (id, name, age, gender) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE name = %s, age = %s, gender = %s"
    val = (row['id'], row['name'], row['age'], row['gender'], row['name'], row['age'], row['gender'])
    cursor.execute(sql, val)

# commit the changes to the database
conn.commit()

# close the connection
conn.close()
