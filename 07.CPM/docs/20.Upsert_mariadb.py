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
data = {'Ma': [5, 9, 7],
        'Ten': ['Duynd21', 'Dungnd18', 'Anth79'], 
        'Tuoi': [20, 35, 21], 
        'Gioi': ['M', 'M', 'M']}
df = pd.DataFrame(data)

# create a cursor object to execute SQL statements
cursor = conn.cursor()

# loop through each row in the DataFrame and insert/update the MySQL table accordingly
for index, row in df.iterrows():
    sql = "INSERT INTO people (id, name, age, gender) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE name = %s, age = %s, gender = %s"
    val = (row['Ma'], row['Ten'], row['Tuoi'], row['Gioi'], row['Ten'], row['Tuoi'], row['Gioi'])
    cursor.execute(sql, val)

# commit the changes to the database
conn.commit()

# close the connection
conn.close()
