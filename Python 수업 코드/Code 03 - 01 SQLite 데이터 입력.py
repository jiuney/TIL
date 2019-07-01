import sqlite3

conn = sqlite3.connect("samsongDB") # 1. DB 연결
cur = conn.cursor() # 2. 커서 생성 (트럭, 연결로프)
sql = "CREATE TABLE IF NOT EXISTS userTable(userId INT, userName CHAR(5))"
cur.execute(sql)

sql = "INSERT INTO userTable VALUES(1, '홍길동')";
cur.execute(sql)
sql = "INSERT INTO userTable VALUES(2, '이순신')";
cur.execute(sql)

cur.close()
conn.commit()
conn.close() # 6. DB 닫기 (=연결 해제)
print ("OK~")