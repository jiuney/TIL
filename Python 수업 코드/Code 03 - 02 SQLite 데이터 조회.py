import sqlite3

conn = sqlite3.connect("samsongDB") # 1. DB 연결
cur = conn.cursor() # 2. 커서 생성 (트럭, 연결로프)
sql = "SELECT * FROM userTable"
cur.execute(sql)

rows = cur.fetchall()

print(rows)

cur.close()
conn.close() # 6. DB 닫기 (=연결 해제)
print ("OK~")