import pymysql

# DB 접속 정보

IP = "192.168.56.110"
USER = "root"
PW = "1234"
DB = "review_DB"
PORT = "3306"


try:
    conn = pymysql.connect(host=IP, user=USER, password=PW, db=DB, charset="utf8")
except:
    print("DB 연결 실패")
    exit()

cur = conn.cursor()

sql = "INSERT INTO emp_tbl (emp_id, emp_name, emp_pay) VALUES (10002, N'이순신', 5000)"
try:
    cur.execute(sql)
except:
    print("입력 실패 - 확인 요망")

conn.commit()

cur.close()
conn.close()