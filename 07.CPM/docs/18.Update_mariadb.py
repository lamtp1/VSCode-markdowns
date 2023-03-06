import mysql.connector
import pandas as pd
 
# connect to the database
cnx = mysql.connector.connect(user='root', password='160299',
                              host='192.168.209.144', port=3306, database='cpm')
cursor = cnx.cursor()

# create dataframe
data = {'name': ['Bob', 'John'],
        'age': [50, 55],
        'gender': ['M', 'F']}
df = pd.DataFrame(data)

# loop through each row in the DataFrame and update the MySQL table accordingly
for index, row in df.iterrows():
    sql = "UPDATE people SET age = %s, gender = %s WHERE name = %s"
    val = (row['age'], row['gender'], row['name'])
    cursor.execute(sql, val)

# commit the changes to the database
cnx.commit()

# close the cursor and database connection
cursor.close()
cnx.close()
