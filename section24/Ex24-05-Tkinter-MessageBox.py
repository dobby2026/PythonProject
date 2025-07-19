'''
파일명: Ex24-05-Tkinter-MessageBox.py
'''

import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title('메시지박스 예제')
root.geometry('500x300')

def show_info():
    messagebox.showinfo('정보', '정보 메시지 입니다.')

def show_warning():
    messagebox.showwarning('경고', '경고 메시지 입니다.')

def show_error():
    messagebox.showerror('오류', '오류 메시지 입니다.')

def show_question():
    result = messagebox.askquestion('질문', '계속하시겠습니까?')
    print(f'응답: {result}')

def show_okcancel():
    result = messagebox.askokcancel('확인', '변경사항을 저장하시겠습니까?')
    print(f'응답: {result}')

tk.Button(root, text='정보 메시지', command=show_info).pack(pady=5)
tk.Button(root, text='경고 메시지', command=show_warning).pack(pady=5)
tk.Button(root, text='오류 메시지', command=show_error).pack(pady=5)
tk.Button(root, text='질문 메시지', command=show_question).pack(pady=5)
tk.Button(root, text='확인/취소 메시지', command=show_okcancel).pack(pady=5)

root.mainloop()