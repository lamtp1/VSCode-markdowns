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
data = {'Ma': [304, 404, 504],
        'Ten': ['Duynd214', 'Dungnd184', 'Anth794'], 
        'Tuoi': [204, 354, 214], 
        'Gioi': ['M4', 'M4', 'M4']}
df = pd.DataFrame(data)

# create a cursor object to execute SQL statements
cursor = conn.cursor()

# loop through each row in the DataFrame and insert/update the MySQL table accordingly, data=val
for index, row in df.iterrows():
    sql = "INSERT INTO people (id, name, age, gender) VALUES (%s,%s,%s,%s) "
    val = (row['Ma'], row['Ten'], row['Tuoi'], row['Gioi'])
    cursor.execute(sql, val)

# commit the changes to the database
conn.commit()

# close the connection
conn.close()
