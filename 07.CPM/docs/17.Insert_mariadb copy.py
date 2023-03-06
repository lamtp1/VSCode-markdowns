import mysql.connector
import pandas as pd
 

# connect to the database
cnx = mysql.connector.connect(user='root', password='160299',
                              host='192.168.209.144', port=3306, database='cpm')
cursor = cnx.cursor()
table_name = 'people'

# insert the data into the table
data = {'name': ['Duynd21', 'Linhnd47', 'Anth79'],
        'age': [25, 24, 26],
        'gender': ['M', 'M', 'M']}
df = pd.DataFrame(data)

# cho VALUES de cac bien trong phan data{}, ten khi khai bao data co the khac ten cot cua table
insert_query = f"INSERT INTO {table_name} (name, age, gender) VALUES (%s, %s, %s)"
for row in df.itertuples(index=False):
    cursor.execute(insert_query, row)

# commit the changes to the database
cnx.commit()

# close the cursor and database connection
cursor.close()
cnx.close()
