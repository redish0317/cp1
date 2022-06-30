import psycopg2
import pandas as pd
from sqlalchemy import create_engine # sql에 csv파일 보내기

host = host="heffalump.db.elephantsql.com"
database="kyndpfqh"
user="kyndpfqh"
password="oVto9ymfg0TXiBFe7Ryo6J1BCVInAwG4"

conn = psycopg2.connect( # 커넥션 생성
    host=host,
    user=user,
    password=password,
    database=database
)

cur = conn.cursor() # 커서 생성

wanted_file = pd.read_csv('wanted2.csv')
engine = create_engine('postgresql://kyndpfqh:oVto9ymfg0TXiBFe7Ryo6J1BCVInAwG4@heffalump.db.elephantsql.com/kyndpfqh')

wanted_file.to_sql("wanted2", engine)

conn.commit()