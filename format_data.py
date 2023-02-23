from get_people import start_db, close_db
import pandas as pd


conn = start_db()
df = pd.read_sql("select * from people", conn)
conn.commit()
conn.close()
print(df.dtypes)
