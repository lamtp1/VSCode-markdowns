import mysql.connector
import pandas as pd
 
data = {'name': ['Duynd21', 'Linhnd47', 'Anth79'],
        'age': [25, 24, 26],
        'gender': ['M', 'M', 'M']}
df = pd.DataFrame(data)

df_string = df.to_string(index=False)
print(df_string)


