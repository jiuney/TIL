import pymysql



## DB 정보 ##

myIP = "192.168.56.110"
myUSER = "root"
myPW = "1234"
myDB = "quiz_db"



## DB 연결 및 데이터 입력

conn = pymysql.connect(host = myIP, user = myUSER, password = myPW, db = myDB, charset = "utf8")
cur = conn.cursor()

while True:
    s_id = str(input("아이디를 입력해주세요: "))
    if s_id == "":
        break
    s_ssn = str(input("주민번호를 입력해주세요: "))
    s_email = str(input("이메일을 입력해주세요: "))

    sql = "INSERT INTO quiz_tbl(student_id, student_ssn, student_email) VALUES ('{}', {}, '{}')".format(s_id, s_ssn, s_email)

    cur.execute(sql)
    conn.commit()

cur.close()
conn.close()