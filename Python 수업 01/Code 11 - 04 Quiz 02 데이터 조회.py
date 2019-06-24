import pymysql



## DB 정보 ##

myIP = "192.168.56.110"
myUSER = "root"
myPW = "1234"
myDB = "quiz_db"



## DB 연결 및 데이터 조회

conn = pymysql.connect(host = myIP, user = myUSER, password = myPW, db = myDB, charset = "utf8")
cur = conn.cursor()

sql = "SELECT student_id, student_ssn, student_email FROM quiz_tbl"
cur.execute(sql)

print("아이디", "\t\t", "주민번호", "\t\t", "이메일")
print("-------------------------------------")

while True:
    row = cur.fetchone()
    if row == None:
        break
    print(row[0], "\t\t", row[1], "\t\t", row[2])

cur.close()
conn.close()