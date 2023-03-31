import mysql.connector
import pandas as pd
 

# connect to the database
cnx = mysql.connector.connect(user='root', password='123',
                              host='10.205.35.216', port=3306, database='CPM')
cursor = cnx.cursor()

# create the table in the database
table_name = 'people'
# create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (name VARCHAR(255), age INT, gender CHAR(1))"
# cursor.execute(create_table_query)

# insert the data into the table
data = {'name': ['John', 'Jane', 'Bob'],
        'age': [25, 30, 36],
        'gender': ['M', 'F', 'M']}
df = pd.DataFrame(data)
insert_query = f"INSERT INTO {table_name} (name, age, gender) VALUES (%s, %s, %s)"
for row in df.itertuples(index=False):
    cursor.execute(insert_query, row)

# commit the changes to the database
cnx.commit()

# close the cursor and database connection
cursor.close()
cnx.close()
