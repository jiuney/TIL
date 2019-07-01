import pymysql

# DB 접속 정보

IP = "192.168.56.110"
USER = "root"
PW = "1234"
DB = "review_DB"
PORT = "3306"



conn = pymysql.connect(host=IP, user=USER, password=PW, db=DB, charset="utf8")
cur = conn.cursor()

sql = "SELECT emp_id, emp_name, emp_pay FROM emp_tbl"
cur.execute(sql)

# rows = cur.fetchall()
# for row in rows:
#     print(row[0], row[1], row[2])

while True:
    row = cur.fetchone()
    if row is None:
        break
    print(row[0], row[1], row[2])

cur.close()
conn.close()