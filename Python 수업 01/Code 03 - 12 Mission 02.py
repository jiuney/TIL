import pymysql

conn = pymysql.connect(host="192.168.56.106", user="root", password="1234", db="mission03", charset="utf8")
cur = conn.cursor()
sql = "SELECT * FROM missionTable"
cur.execute(sql)

print("사번 이름 입사연도")
print("-----------------")

while True:
    recs = cur.fetchone()
    if recs == None:
        break
    print(recs[0], recs[1], recs[2])

print("-----------------")

cur.close()
conn.close()
