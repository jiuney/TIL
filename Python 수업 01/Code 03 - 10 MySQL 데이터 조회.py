import pymysql

conn = pymysql.connect(host="192.168.56.107", user="root", password="1234", db="samsongDB", charset="utf8") # 1. DB 연결
cur = conn.cursor() # 2. 커서 생성 (트럭, 연결로프)
sql = "SELECT * FROM userTable2"
cur.execute(sql)

rows = cur.fetchall()

print(rows)

cur.close()
conn.close() # 6. DB 닫기 (=연결 해제)
print ("OK~")