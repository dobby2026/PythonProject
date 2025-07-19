"""
파일명: Ex24-02-Tkinter-Canvas.py
"""

from tkinter import *
import time

root = Tk()
# Canvas 위젯 생성
canvas = Canvas(root, width=500, height=500)
canvas.pack()

# 다각형 그리기
canvas.create_polygon(250, 400, 275, 450, 225, 450)
canvas.create_polygon(250, 400, 275, 450, 225, 450)

for i in range(0, 70):
    canvas.move(1, -5, -5)
    canvas.move(2, 5, -5)

    root.update()
    time.sleep(0.05)

# 실행코드
root.mainloop()