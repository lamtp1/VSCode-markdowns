import mysql.connector
import pandas as pd
 

# connect to the database
cnx = mysql.connector.connect(user='root', password='160299',
                              host='192.168.209.144', port=3306, database='cpm')
cursor = cnx.cursor()

# create the table in the database
# table_name = 'people'
# create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (name VARCHAR(255), age INT, gender CHAR(1))"
# cursor.execute(create_table_query)

# insert the data into the table
data = {'name': ['Bob', 'John'],
        'age': [40, 50],
        'gender': ['M', 'F']}
df = pd.DataFrame(data)

# df_string = df.to_string(index=False)
# print(df_string)

# cho VALUES de cac bien trong phan data{}, ten data co the khac ten cot cua table
# insert_query = f"INSERT INTO {table_name} (name, age, gender) VALUES (%s, %s, %s)"
# for row in df.itertuples(index=False):
#     cursor.execute(insert_query, row)

# loop through each row in the DataFrame and update the MySQL table accordingly
for index, row in df.iterrows():
    sql = "UPDATE people SET age = %s, gender = %s WHERE name = %s"
    val = (row['name'], row['age'], row['gender'])
    cursor.execute(sql, val)

# commit the changes to the database
cnx.commit()

# close the cursor and database connection
cursor.close()
cnx.close()
