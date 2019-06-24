import pymysql

conn = pymysql.connect(host="192.168.56.106", user="root", password="1234", db="mission03", charset="utf8")
cur = conn.cursor()
sql = "CREATE TABLE IF NOT EXISTS missionTable(cin INT, name CHAR(5), eYear SMALLINT)"
cur.execute(sql)

while True:
    cinnum = int(input("사번 --> "))
    if cinnum == 0:
        break
    empname = input("이름 --> ")
    empyear = int(input("입사연도 --> "))
    sql = "INSERT INTO missionTable VALUES({0:d}, '{1:s}', {2:d})".format(cinnum, empname, empyear)    # 큰따옴표와 작은따옴표는 큰 차이가 있다!
    cur.execute(sql)
    conn.commit()

cur.close()
conn.close()
print("끝!")
