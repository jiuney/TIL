##### Quiz2. Code 09-05으로 선택된 CSV를 Treeview로 출력하기

import csv
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *

window = Tk()
window.geometry("800x500")

sheet = ttk.Treeview(window)



csvList = []
with open("C:/images/csv/emp.csv") as rfp:
    reader = csv.reader(rfp)
    headerList = next(reader)
    for cList in reader:
        csvList.append(cList)



# 트리뷰 첫번째 열 만들기
sheet.column("#0", width=70)    # 첫 컬럼의 내부 이름
sheet.heading("#0", text="ID")    # 첫 컬럼의 표시될 이름

# 두번째 이후 열 만들기
sheet["columns"] = ("H1", "H2", "H3", "H4")    # 두번째 이후 컬럼의 내부 이름 (내맘대로)
sheet.column("H1", width=70)
sheet.heading("H1", text="%s" % (headerList[0]))    # 각 컬럼의 표시될 이름
sheet.column("H2", width=70)
sheet.heading("H2", text="%s" % (headerList[1]))
sheet.column("H3", width=70)
sheet.heading("H3", text="%s" % (headerList[2]))
sheet.column("H4", width=70)
sheet.heading("H4", text="%s" % (headerList[3]))

# 내용 채우기
for i in range(len(csvList)):
    sheet.insert("", "end", text="%d열값" % (i+1), values=("%s" % (str(csvList[i][0])), "%s" % (str(csvList[i][1])), "%s" % (str(csvList[i][2])), "%s" % (str(csvList[i][3]))))

sheet.pack()
window.mainloop()


