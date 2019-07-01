from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *

## 전역변수 선언부 ##
# dirName = "C:/images/Pet_GIF/Pet_GIF(256x256)/"
# fnameList = [ "cat01_256.gif","cat02_256.gif","cat03_256.gif",
#               "cat04_256.gif","cat05_256.gif","cat06_256.gif"]
fnameList = []
import os


photoList = [None] * 6
num = 0 # 현재 사진 순번
## 함수 선언부
def keyPress(e) :
    global  num
    # keycode number" 등으로 검색해서 키코드 번호 확인
    if e.keycode == 36 : #Home
        num = 0
    if e.keycode == 35 : #End
        num = len(fnameList)-1
    if 49 <= e.keycode <= 57 : # 1~9
        num = num + e.keycode - 48
        if num > len(fnameList)-1 :
            num = len(fnameList) - 1

    photo = PhotoImage(file=fnameList[num])
    pLabel.configure(image=photo)
    pLabel.photo=photo

def clickPrev() :
    global num
    num -= 1
    if num < 0:
        num = len(fnameList)-1
    photo = PhotoImage(file=fnameList[num])
    pLabel.configure(image=photo)
    pLabel.photo = photo

def clickNext() :
    global num
    num += 1
    if num >= len(fnameList) :
        num = 0
    photo = PhotoImage(file=fnameList[num])
    pLabel.configure(image=photo)
    pLabel.photo=photo


def hopImage(count=0) :
    if count==0 :
        count = askinteger("건너뛸 수", "숫자-->")
    for _ in range(count) :
        clickNext()


def selectFile() :
    filename = askopenfilename(parent=window,
             filetypes=(("GIF파일", "*.gif;*.raw"), ("모든파일", "*.*")))
    print(filename)
    pLabel.configure(text=str(filename))
    pLabel.text=filename

## 메인 코드부
window = Tk()
window.title('GIF 사진 뷰어 Beta (Ver 0.01)')
window.geometry("500x300")
window.resizable(width=FALSE, height=TRUE)

folder = askdirectory(parent=window)
for dirName, subDirList, fnames in os.walk(folder) :
    for fname in fnames:
        if os.path.splitext(fname)[1].upper() == '.GIF' :
            fullName = dirName + '/' + fname
            fnameList.append(fullName)


print(fnameList[num])
photo = PhotoImage(file = fnameList[num])
pLabel = Label(window, image=photo)

btnPrev = Button(window, text='<< 이전 그림', command=clickPrev)
btnNext = Button(window, text='다음 그림>>', command=clickNext)

window.bind("<Key>", keyPress)

mainMenu = Menu(window)
window.config(menu=mainMenu)

moveMenu = Menu(mainMenu)
mainMenu.add_cascade(label='이동', menu=moveMenu)
moveMenu.add_command(label='앞으로', command=clickPrev)
moveMenu.add_separator()
moveMenu.add_command(label='뒤로', command=clickNext)

hopMenu = Menu(mainMenu)
mainMenu.add_cascade(label='건너뛰기', menu=hopMenu)
hopMenu.add_command(label='1', command=lambda : hopImage(1))
hopMenu.add_command(label='3', command=lambda : hopImage(3))
hopMenu.add_command(label='5', command=lambda : hopImage(5))
hopMenu.add_command(label='원하는 수', command=hopImage)
hopMenu.add_separator()
hopMenu.add_command(label='파일 선택', command=selectFile)


btnPrev.place(x=150, y=10); btnNext.place(x=250, y=10)
pLabel.place(x=15, y=50)
window.mainloop()