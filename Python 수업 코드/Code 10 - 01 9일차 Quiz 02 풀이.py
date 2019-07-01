##### Quiz2. Code 09-05으로 선택된 CSV를 Treeview로 출력하기

import csv
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *

def openCSV():
    global csvList
    filename = askopenfilename(parent=window,
                               filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    csvList = []
    with open(filename) as rfp:
        reader = csv.reader(rfp)
        headerList = next(reader)
        sum = 0
        count = 0
        for cList in reader:
            csvList.append(cList)

    sheet = ttk.Treeview(window)

    # 기존 시트 클리어
    sheet.delete(*sheet.get_children())

    # 트리뷰 첫번째 열 만들기
    sheet.column("#0", width=70)  # 첫 컬럼의 내부 이름
    sheet.heading("#0", text=headerList[0])  # 첫 컬럼의 표시될 이름

    # 두번째 이후 열 만들기
    sheet["columns"] = headerList[1:]  # 두번째 이후 컬럼의 내부 이름 (내맘대로)
    for colName in headerList[1:]:
        sheet.column(colName, width=70)
        sheet.heading(colName, text=colName)

    # 내용 채우기
    for row in csvList:
        sheet.insert("", "end", text=row[0], values=row[1:])

    sheet.pack(expand=1, anchor=CENTER)

window = Tk()
window.geometry("400x500")

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="CSV 처리", menu=fileMenu)
fileMenu.add_command(label="CSV 열기", command=openCSV)

window.mainloop()
